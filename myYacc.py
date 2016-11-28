from ply import yacc
from myLex import tokens, MyLexer
from myUtils import *

lexer = MyLexer(optimize=True)
# lexer = MyLexer()


def parser():
    def p_sentence(p):
        """sentence: question
                   | rule
                   | fact"""
        p[0] = p[1]
        return p[0]

    def p_question(p):
        """question : QUESTION query"""
        p[0] = p[2]

    def p_query(p):
        """query : PREDICATE LPAREN arguments RPAREN
                 | NOT query"""
        if len(p) == 5:
            p[0] = Query(p[1], p[3])
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
                | clause AND clause
                | clause OR clause
                | LPAREN rule RPAREN AND clause
                | LPAREN rule RPAREN OR clause
                | clause AND LPAREN rule RPAREN
                | clause OR LPAREN rule RPAREN
                | rule IMPLIES clause
                | LPAREN rule RPAREN
                | NOT LPAREN rule RPAREN"""
        def and_rule(_rule, clause):
            if "AND" in _rule:
                _rule["AND"].append(clause)
            elif "OR" in _rule:
                for r in _rule["OR"]:
                    r.append(clause)
            return _rule

        def or_rule(_rule, clause):
            new_list = []
            new_list.append(clause)
            if "AND" in _rule:
                new_rule = {"OR": [new_list, _rule["AND"]]}
                return new_rule
            elif "OR" in _rule:
                _rule["OR"].append(new_list)
                return _rule

        def not_rule(_rule):
            if "AND" in _rule:
                _rule["OR"] = []
                for item in _rule["AND"]:
                    item.inverse()
                    _rule["OR"].append([item])
                del _rule["AND"]
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
                for line in _rule["OR"]:
                    lens.append(len(line))
                    record.append(0)
                    for item in line:
                        item.inverse()
                matrix = []
                bfs(_rule["OR"], matrix, len(lens), record, lens)
                _rule["OR"] = matrix
                return _rule

        if len(p) == 2:
            p[0] = {"AND": [p[1]]}
        elif len(p) == 4 and p[2] == '&':  # clause AND clause
            p[0] = {"AND": [p[1], p[3]]}
        elif len(p) == 4 and p[2] == '|':  # clause OR clause
            p[0] = {"OR": [[p[1]], [p[3]]]}
        elif len(p) == 6 and p[4] == '&':  # LPAREN rule RPAREN AND clause
            p[0] = and_rule(p[2], p[5])
        elif len(p) == 6 and p[4] == '|':  # LPAREN rule RPAREN OR clause
            p[0] = or_rule(p[2], p[5])
        elif len(p) == 6 and p[2] == '&':  # clause AND LPAREN rule RPAREN
            p[0] = and_rule(p[4], p[1])
        elif len(p) == 6 and p[2] == '|':  # clause OR LPAREN rule RPAREN
            p[0] = or_rule(p[4], p[1])
        elif len(p) == 4 and p[2] == '=>':  # rule = rule => clause
            rule = not_rule(p[1])
            p[0] = or_rule(rule, p[3])
        elif len(p) == 4 and p[1] == '(':
            p[0] = p[2]
        elif len(p) == 5 and p[1] == '~':
            p[0] = not_rule(p[3])
        else:
            print(len(p))

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

