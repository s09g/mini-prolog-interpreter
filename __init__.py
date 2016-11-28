#! /usr/bin/env python3
from myYacc import lexer, parser

MyParser = parser()

fact = {}
rule = []

s = input()
while s != "exit":
    lexer.input(s)
    ast = MyParser.parse(s)
    if isinstance(ast, Fact):
        if ast.predicate in fact:
            fact[ast.predicate].append(ast)
        else:
            fact[ast.predicate] = [ast]
    elif isinstance(ast,Query):
        pass
    else:
        rule.append(ast)
    s = input()
