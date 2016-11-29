from ply import yacc
from myLex import tokens, MyLexer
from myUtils import *

# lexer = MyLexer(optimize=True)
lexer = MyLexer()


def parser():
    precedence = (
        ('left', 'AND', 'OR'),
        ('left', 'IMPLIES'),
    )
    def p_sentence(p):
        """sentence : question
                    | rule
                    | fact"""
        p[0] = p[1]

    def p_question(p):
        """question : QUESTION query"""
        p[0] = [2]

    def p_query(p):
        """query : PREDICATE LPAREN arguments RPAREN
                 | NOT query"""
        if len(p) == 5:
            p[0] = Query(p[1]. p[3])
        elif len(p) == 3:
            p[0] = p[2].inverse()
            
    def p_arguments(p):
        """arguments : CONSTANT
                     | arguments COMMA CONSTANT"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]


    def p_rule(p):
        """rule : clause
                | rule OR rule
                | rule AND rule
                | rule IMPLIES rule
                | LPAREN rule RPAREN
                | NOT LPAREN rule RPAREN"""
        def or_rule(_rule, clause):
            if "OR" in _rule:
                _rule["OR"].append(clause)
            elif "AND" in _rule:
                for r in _rule["AND"]:
                    r.append(clause)
            return _rule

        def and_rule(_rule, clause):
            new_list = list()
            new_list.append(clause)
            if "OR" in _rule:
                new_rule = {"AND": [new_list, _rule["OR"]]}
                return new_rule
            elif "AND" in _rule:
                _rule["AND"].append(new_list)
                return _rule

        def not_rule(_rule):
            if "OR" in _rule:
                _rule["AND"] = []
                for item in _rule["OR"]:
                    item.inverse()
                    _rule["AND"].append([item])
                del _rule["OR"]
                return _rule
            else:
                def bfs(src, goal, l, crt_rec, end):
                    new_line = []
                    for i in range(l):
                        new_line.append(src[i][crt_rec[i]])
                    goal.append(new_line)

                    for i in range(l):
                        crt_rec[i] += 1
                        if crt_rec[i] < end[i]:
                            bfs(src, goal, l, crt_rec, end)
                        crt_rec[i] -= 1

                lens = []
                record = []
                for line in _rule["AND"]:
                    lens.append(len(line))
                    record.append(0)
                    for item in line:
                        item.inverse()
                matrix = []
                bfs(_rule["AND"], matrix, len(lens), record, lens)
                _rule["AND"] = matrix
                return _rule

        def rule_or_rule(r1, r2):
            if "OR" in r1:
                for clause in r1["OR"]:
                    r2 = or_rule(r2, clause)
            elif "OR" in r2:
                for clause in r2["OR"]:
                    r2 = or_rule(r1, clause)
            else:
                for line in r1["AND"]:
                    r2 = rule_or_rule({"OR": line}, r2)
            return r2

        def rule_and_rule(r1, r2):
            if "OR" in r1:
                for clause in r1["OR"]:
                    r2 = and_rule(r2, clause)
            elif "OR" in r2:
                for clause in r2["OR"]:
                    r2 = and_rule(r2, clause)
            else:
                r2["AND"].extend(r1["AND"])
            return r2

        if len(p) == 2:
            p[0] = {"OR": [p[1]]}
        elif p[2] == '|':
            p[0] = rule_or_rule(p[1], p[3])
        elif p[2] == '&':
            p[0] = rule_and_rule(p[1], p[3])
        elif p[2] == '=>':
            rule = not_rule(p[1])
            p[0] = rule_or_rule(rule, p[3])
        elif p[1] == '(':
            p[0] = p[2]
        elif p[1] == '~':
            p[0] = not_rule(p[3])


    def p_clause(p):
        """clause : PREDICATE LPAREN variables RPAREN
                  | NOT clause"""
        if len(p) == 5:
            p[0] = Clause(p[1], p[3])
        elif len(p) == 3:
            p[0] = p[2].inverse()

    def p_variables(p):
        """variables : VARIABLE
                     | variables COMMA VARIABLE"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]

    def p_fact(p):
        """fact : PREDICATE LPAREN constants RPAREN
                | NOT fact
                | LPAREN fact RPAREN"""
        if len(p) == 5:
            p[0] = Fact(p[1], p[3])
        elif len(p) == 3:
            p[0] = p[2].inverse()
        elif len(p) == 4:
            p[0] = p[2]

    def p_constants(p):
        """constants : CONSTANT
                     | constants COMMA CONSTANT"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]

    def p_error(p):
        print("Syntax error at '%s'" % p.value)

    return yacc.yacc()
