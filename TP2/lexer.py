import ply.lex as lex
import sys

reserved = {
    'int' : 'INT',
    'array' : 'ARRAY',
    'matrix' : 'MATRIX',
    'sum' : 'SUM',
    'subtrac' : 'SUBTRAC',
    'mult' : 'MULT',
    'div' : 'DIV',
    'rem' : 'REM',
    'gt' : 'GT',
    'lt' : 'LT',
    'gte' : 'GTE',
    'lte' : 'LTE',
    'equals' : 'EQUALS',
    'notequals' : 'NOTEQUALS',
    'not' : 'NOT',
    'and' : 'AND',
    'or' : 'OR',
    'write' : 'WRITE',
    'read' : 'READ',
    'while' : 'WHILE',
    'do' : 'DO',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE'
}


tokens = [
        'NUM',
        'NAME',
        'ATRIB',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'COMMA',
        'DOTCOMMA'
] + list(reserved.values())


t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r'\,'
t_DOTCOMMA = r'\;'


def t_NUM(t):
    r'\d+'
    return t

def t_NAME(t):
    r'[a-z]+\w*'
    return t

def t_ATRIB(t):
    r'\='
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def lexer_build():
    lexer = lex.lex()
    return lexer