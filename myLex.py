from ply import lex

tokens = (
    'CONSTANT',
    'PREDICATE',
    'NOT',
    'OR',
    'AND',
    'IMPLIES',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'VARIABLE',
    'QUESTION',
)

def MyLexer(optimize=False):
    t_NOT = r'~'
    t_OR = r'\|'
    t_AND = r'&'
    t_IMPLIES = r'=>'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_QUESTION = r'\?-'
    t_COMMA = r','
    t_PREDICATE = r'[A-Z]\w*(?=\()'
    t_CONSTANT = r'[A-Z]\w*'
    t_VARIABLE = r'[a-z]'
    t_ignore = ' \t'


    def t_newline(t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    return lex.lex(optimize=optimize)