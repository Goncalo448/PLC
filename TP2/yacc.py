import ply.yacc as yacc
from lexer import *
import sys


def p_Program(p):
    'Program : Declarations Body'
    p[0] = p[1] + "START\n" + p[2] + "STOP\n"


def p_Program_noDeclarations(p):
    'Program : Body'
    p[0] = "START\n" + p[1] + "STOP\n"


def p_Declarations_single(p):
    'Declarations : Declaration'
    p[0] = p[1]


def p_Declarations_multiple(p):
    'Declarations : Declaration Declarations'
    p[0] = p[1] + p[2]


def p_Declaration_Int(p):
    'Declaration : INT NAME DOTCOMMA'
    if p[2] not in p.parser.fp:
        p.parser.fp.update({p[2]: p.parser.gp})
        p[0] = "PUSHI 0\n"
        p.parser.gp += 1
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[2]} already declared!")
        raise SyntaxError
        #parser.success = False
        #VERIFICAR DE QUE FORMA MANIPULAR OS ERROS


def p_Declaration_Array(p):
    'Declaration : ARRAY LBRACKET NUM RBRACKET NAME DOTCOMMA'
    if p[5] not in p.parser.fp:
        p.parser.fp.update({p[5]: (p.parser.gp, int(p[3]))})
        p[0] = f"PUSHN {p[3]}\n"
        p.parser.gp += int(p[3])
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[5]} already declared!")
        raise SyntaxError


def p_Declaration_Matrix(p):
    'Declaration : MATRIX LBRACKET NUM RBRACKET LBRACKET NUM RBRACKET NAME DOTCOMMA'
    if p[8] not in p.parser.fp:
        p.parser.fp.update({p[8]: (p.parser.gp, int(p[3]), int(p[6]))})
        n = int(p[3]) * int(p[6])
        p[0] = f"PUSHN {str(n)}\n"
        p.parser.gp += n
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[8]} already declared!")
        raise SyntaxError


def p_Body_single(p):
    'Body : Process'
    p[0] = p[1]


def p_Body_multiple(p):
    'Body : Process Body'
    p[0] = p[1] + p[2]


def p_Process(p):
    '''Process : Ite
               | WhileLoop
               | Write_stdout
               | Assignment'''
    p[0] = p[1]


def p_If_Then(p):
    'Ite : IF condition THEN Body DOTCOMMA'
    p[0] = p[2] + f'JZ l{p.parser.labels}\n' + p[4] + f'l{p.parser.labels}: NOP\n'
    p.parser.labels += 1


def p_If_Then_Else(p):
    'Ite : IF condition THEN Body ELSE Body DOTCOMMA'
    p[0] = p[2] + f'JZ l{p.parser.labels}\n' + p[4] + f'JUMP l{p.parser.labels}f\nl{p.parser.labels}: NOP\n' + p[6] + f'l{p.parser.labels}f: NOP\n'
    p.parser.labels += 1


def p_While(p):
    'WhileLoop : WHILE condition DO Body DOTCOMMA'
    p[0] = f'l{p.parser.labels}c: NOP' + p[2] + f'JZ l{p.parser.labels}f\n' + p[4] + f'JUMP l{p.parser.labels}c\nl{p.parser.labels}f: NOP\n'
    p.parser.labels += 1


def p_Write_Array_Matrix(p):
    'Write_stdout : WRITE NAME DOTCOMMA'
    if p[2] not in p.parser.fp:
        var = p.parser.fp.get(p[2])

        if type(var) == tuple:
            if len(var) == 2:
                array = f'PUSHS "[ "\nWRITES\n'
                for i in range(var[1]):
                    array += f'PUSHGP\nPUSHI {var[0]}\nPADD\nPUSHI {i}\nLOADN\nWRITEI\nPUSHS " "\nWRITES\n'
                array += f'PUSHS "]"\nWRITES\n'
                p[0] = array + 'PUSHS "\\n"\nWRITES\n'

            elif len(var) == 3:
                matrix = ""
                for i in range(var[1]):
                    matrix += f'PUSHS "[ "\nWRITES\n'
                    for j in range(var[2]):
                        matrix += f'PUSHGP\nPUSHI {var[0]}\nPADD\nPUSHI {var[2] * i + j}\nLOADN\nWRITEI\nPUSHS " "\nWRITES\n'
                    matrix += 'PUSHS "]\\n"\nWRITES\n'
                p[0] = matrix

    else:
        print(f"Error, line {p.lineno(2)}: variable {p[2]} does not exists!")
        raise SyntaxError


def p_Write_Expr(p):
    'Write_stdout : WRITE Expr'
    p[0] = p[2] + 'WRITEI\nPUSHS "\\n"\nWRITES\n'


def p_Assignment_Expr(p):
    'Assignment : NAME ATRIB Expr DOTCOMMA'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if type(var) == int:
            p[0] = p[3] + f'STOREG {var}\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Int.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assignment_Array(p):
    'Assignment : NAME LBRACKET Expr RBRACKET ATRIB Expr'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 2:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n' + p[3] + p[6] + 'STOREN\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Array.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assignment_Matrix(p):
    'Assignment : NAME LBRACKET Expr RBRACKET LBRACKET Expr RBRACKET ATRIB Expr'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 3:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n{p[3]}PUSHI {var[2]}\nMUL\n{p[6]}ADD\n{p[9]}STOREN\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Matrix.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assignment_Read_Array(p):
    'Assignment : NAME LBRACKET Expr RBRACKET ATRIB READ DOTCOMMA'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 2:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n' + p[3] + f'READ\nATOI\nSTOREN\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Array.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assignment_Read_Matrix(p):
    'Assignment : NAME LBRACKET Expr RBRACKET LBRACKET Expr RBRACKET ATRIB READ DOTCOMMA'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 3:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n' + p[3] + f'PUSHI {var[2]}\nMUL\n' + p[5] + f'ADD\nREAD\nATOI\nSTOREN\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Matrix.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assignment_Read(p):
    'Assignment : NAME ATRIB READ DOTCOMMA'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if type(var) == int:
            p[0] = f'READ\nATOI\nSTOREG {var}\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Int.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_condition_base(p):
    'condition : LPAREN condition RPAREN'
    p[0] = p[2]


def p_condition_compare(p):
    '''condition : GT LPAREN Expr COMMA Expr RPAREN
                 | GTE LPAREN Expr COMMA Expr RPAREN
                 | LT LPAREN Expr COMMA Expr RPAREN
                 | LTE LPAREN Expr COMMA Expr RPAREN
                 | EQUALS LPAREN Expr COMMA Expr RPAREN
                 | NOTEQUALS LPAREN Expr COMMA Expr RPAREN'''

    if p[1] == "gt":
        p[0] = p[3] + p[5] + 'SUP\n'
    elif p[1] == "gte":
        p[0] = p[3] + p[5] + 'SUPEQ\n'
    elif p[1] == "lt":
        p[0] = p[3] + p[5] + 'INF\n'
    elif p[1] == "lte":
        p[0] = p[3] + p[5] + 'INFEQ\n'
    elif p[1] == "equals":
        p[0] = p[3] + p[5] + 'EQUAL\n'
    elif p[1] == "notequals":
        p[0] = p[3] + p[5] + 'EQUAL\nNOT\n'


def p_condition_logic(p):
    '''condition : NOT LPAREN Expr RPAREN
                 | AND LPAREN Expr COMMA Expr RPAREN
                 | OR LPAREN Expr COMMA Expr RPAREN'''
    
    if p[1] == "not":
        p[0] = p[3] + 'NOT\n'
    elif p[1] == "and":
        p[0] = p[3] + p[5] + 'ADD\nPUSHI 2\nEQUAL\n'
    elif p[1] == "or":
        p[0] = p[3] + p[5] + 'ADD\nPUSHI 1\nSUPEQ\n'


def p_Expr_base(p):
    'Expr : LPAREN Expr RPAREN'
    p[0] = p[2]


def p_Expr_condition(p):
    'Expr : condition'
    p[0] = p[1]


def p_Expr_Num(p):
    'Expr : NUM'
    p[0] = f'PUSHI {p[1]}\n'


def p_Expr_Var(p):
    'Expr : Var'
    p[0] = p[1]


def p_Expr_Arithmetic(p):
    '''Expr : SUM LPAREN Expr COMMA Expr RPAREN 
            | SUBTRAC LPAREN Expr COMMA Expr RPAREN
            | MULT LPAREN Expr COMMA Expr RPAREN
            | DIV LPAREN Expr COMMA Expr RPAREN
            | REM LPAREN Expr COMMA Expr RPAREN'''
    
    if p[1] == "sum":
        p[0] = p[3] + p[5] + 'ADD\n'
    elif p[1] == "subtrac":
        p[0] = p[3] + p[5] + 'SUB\n'
    elif p[1] == "mult":
        p[0] = p[3] + p[5] + 'MUL\n'
    elif p[1] == "div":
        p[0] = p[3] + p[5] + 'DIV\n'
    elif p[1] == "rem":
        p[0] = p[3] + p[5] + 'MOD\n'


def p_Var_Num(p):
    'Var : NAME'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if type(var) == int:
            p[0] = f'PUSHG {var}\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Int.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} doesn't exists.")
        raise SyntaxError


def p_Var_Array(p):
    'Var : NAME LBRACKET Expr RBRACKET'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 2:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n' + p[3] + 'LOAD\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Array.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} doesn't exists.")
        raise SyntaxError


def p_Var_Matrix(p):
    'Var : NAME LBRACKET Expr RBRACKET LBRACKET Expr RBRACKET'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 3:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n' + p[3] + f'PUSHI {var[2]}\nMUL\n' + p[6] + 'ADD\nLOADN\n'
        else:
            print(f"Error, line {p.lineno(2)}: variable {p[1]} isn't of type Matrix.")
            raise TypeError
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} doesn't exists.")
        raise SyntaxError


def p_error(p):
    print(f"Syntax error: token {p.value} on line {p.lineno}.")
    print(p)

#to build the parser call yacc.yacc()
#parser = yacc.yacc()
#frame pointer aponta para o endereço de base das vars locais
#parser.fp = {}
#contem o endereço de base das vars locais
#parser.gp = 0
#parser.labels = 0


def build_parser():
    parser = yacc.yacc()
    parser.fp = dict()
    parser.labels = 0
    parser.gp = 0

    return parser

