import ply.lex as lex
import sys

tokens = (
        'NUM',
        'NAME',
        'INT',
        'ARRAY',
        'MATRIX',
        'SUM',
        'SUBTRAC',
        'MULT',
        'DIV',
        'REM',
        'GT',
        'LT',
        'EQUALS',
        'GTE',
        'LTE',
        'NOTEQUALS',
        'NOT',
        'AND',
        'OR',
        'WRITE',
        'READ',
        'ATRIB',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'WHILE',
        'DO',
        'IF',
        'THEN',
        'ELSE',
        'COMMA',
        'DOTCOMMA'
)


t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r'\,'
t_DOTCOMMA = r'\;'


def t_NUM(t):
    r'\d+'
    return t

def t_INT(t):
    r'(?i:int)'
    return t

def t_NAME(t):
    r'\w+'
    return t

def t_ARRAY(t):
    r'(?i:array)'
    return t

def t_MATRIX(t):
    r'(?i:matrix)'
    return t

def t_SUM(t):
    r'(?i:sum)'
    return t

def t_SUBTRAC(t):
    r'(?i:subtrac)'
    return t

def t_MULT(t):
    r'(?i:mult)'
    return t

def t_DIV(t):
    r'(?i:div)'
    return t

def t_REM(t):
    r'(?i:rem)'
    return t

def t_GT(t):
    r'(?i:gt)'
    return t

def t_LT(t):
    r'(?i:lt)'
    return t

def t_EQUALS(t):
    r'(?i:equals)'
    return t

def t_GTE(t):
    r'(?i:gte)'
    return t

def t_LTE(t):
    r'(?i:lte)'
    return t

def t_NOTEQUALS(t):
    r'(?i:notequals)'
    return t

def t_NOT(t):
    r'(?i:not)'
    return t

def t_AND(t):
    r'(?i:and)'
    return t

def t_OR(t):
    r'(?i:or)'
    return t

def t_WRITE(t):
    r'(?i:write)'
    return t

def t_READ(t):
    r'(?i:read)'
    return t

def t_ATRIB(t):
    r'='
    return t

def t_WHILE(t):
    r'(?i:while)'
    return t

def t_DO(t):
    r'(?i:do)'
    return t

def t_IF(t):
    r'(?i:if)'
    return t

def t_THEN(t):
    r'(?i:then)'
    return t

def t_ELSE(t):
    r'(?i:else)'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()