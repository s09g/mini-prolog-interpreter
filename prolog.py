#! /usr/bin/env python3
from myYacc import lexer, parser
from pprint import pprint
from myUtils import Fact, Query, Rule, MyQueue


MyParser = parser()
raw_query, raw_sentence = get_input()

fact_table = {}
rule_table = {}
query_list = []
answer_list = []


def add_rule(_rules, _line):
    rule = Rule(_line)
    keys = rule.index.keys()
    for key in keys:
        if key not in _rules:
            _rules[key] = []
        _rules[key].append(rule)

for s in raw_sentence:
    result = MyParser.parse(s, lexer=lexer)
    if isinstance(result, Fact):
        res_pre = result.predicate
        if res_pre in fact_table:
            fact_table[res_pre].append(result)
        else:
            fact_table[res_pre] = [result]
    else:
        if "OR" in result:
            add_rule(rule_table, result["OR"])
        else:
            for line_of_or in result["AND"]:
                add_rule(rule_table, line_of_or)

for q in raw_query:
    result = MyParser.parse(q, lexer=lexer)
    query_list.append(result)


def check_clause(clause, fact):
    predicate = clause.predicate
    if predicate not in fact:
        return False
    related_facts = fact[predicate]
    for related_fact in related_facts:
        if related_fact.positive != clause.positive:
            continue
        if str(related_fact) == str(clause):
            return True
    return False



def unify_same_pre(clause, query, query_theta):
    theta = {}
    for i in range(len(query.arguments)):
        argument = clause.arguments[i]
        if query_theta:
            parameter = query_theta[query.arguments[i]]
        else:
            parameter = query.arguments[i]
        if argument not in theta:
            theta[argument] = parameter
        else:
            if theta[argument] != parameter:
                return None
    return theta


def get_related_new_query(a, rules, visited):
    new_query_list = []
    a_pre = a.predicate
    if a_pre not in rules:
        return new_query_list
    related_rules = rules[a_pre]
    for related_rule in related_rules:
        visited.add(related_rule)
        pre_clauses = related_rule.index[a_pre]
        for clause in pre_clauses:
            if clause.positive == a.positive:
                continue
            theta = unify_same_pre(clause, a, None)
            if not theta:
                continue
            else:
                new_query = Query()
                for c in related_rule.clauses:
                    if c is not clause:
                        new_query.clauses.append(c)
                new_query.theta = theta
                new_query.done()
            new_query_list.append(new_query)
    return new_query_list

def get_related_new_query_from_query(query, rules, visited):
    a = query.clauses[0]
    new_query_list = []
    a_pre = a.predicate
    if a_pre not in rules:
        return new_query_list
    related_rules = rules[a_pre]
    for related_rule in related_rules:
        if related_rule in visited:
            continue
        visited.add(related_rule)
        pre_clauses = related_rule.index[a_pre]
        for clause in pre_clauses:
            if clause.positive == a.positive:
                continue
            theta = unify_same_pre(clause, a, query.theta)
            if not theta:
                continue
            else:
                new_query = Query()
                for c in related_rule.clauses:
                    if c is not clause:
                        new_query.clauses.append(c)
                new_query.theta = theta
                new_query.done()
            new_query_list.append(new_query)
    return new_query_list

def check_single_query(query, fact):
    clause = query.clauses[0]
    predicate = clause.predicate
    if predicate not in fact:
        return False
    related_facts = fact[predicate]
    for related_fact in related_facts:
        next_run = False
        if related_fact.positive == clause.positive:
            continue
        for i in range(len(related_fact.arguments)):
            arg = related_fact.arguments[i]
            key = clause.arguments[i]
            if (key not in query.theta) or query.theta[key] != arg:
                next_run = True
                break
        if not next_run:
            return True
    return False

def resolve_single_query(query, visit, fact=fact_table, rules=rule_table):
    if check_single_query(query, fact):
        return True
    unsolved_query = get_related_new_query_from_query(query, rules, visit)

    if not unsolved_query:
        return False

    for query in unsolved_query:
        # print(query)
        next_run = False
        for single_clause in query.clauses:
            single_query = Query()
            single_query.clauses.append(single_clause)
            single_query.theta = query.theta
            single_query.done()
            visit.add(single_query)

            if not resolve_single_query(query, visit, fact, rules):
                next_run = True
                break
        if not next_run:
            return True
    return False




def bc_ask(alpha, fact=fact_table, rules=rule_table):
    if check_clause(alpha, fact):
        return True


    not_alpha = alpha.inverse()
    pre = not_alpha.predicate
    if pre in fact:
        fact[pre].append(not_alpha)
    else:
        fact[pre] = [not_alpha]

    visited_set = set()
    unsolved_query = get_related_new_query(not_alpha, rules, visited_set)

    if not unsolved_query:
        return False

    for query in unsolved_query:

        next_run = False
        for single_clause in query.clauses:
            single_query = Query()
            single_query.clauses.append(single_clause)
            single_query.theta = query.theta
            single_query.done()

            visited_set.add(single_query)
            if not resolve_single_query(single_query, visited_set, fact_table, rule_table):
                next_run = True
                break

        if not next_run:
            return True
    return False


def run(q):
    res = bc_ask(q, fact_table, rule_table)
    del fact_table[q.predicate][-1]
    return res


def resolve_test():
    for q in query_list:
        answer_list.append(run(q))
    # print(answer_list)

resolve_test()
def p_test():
    pprint(fact_table)
    pprint(rule_table)
    pprint(query_list)


