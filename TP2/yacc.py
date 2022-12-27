import ply.yacc as yacc
from lexer import tokens
import sys


def p_Program(p):
    'Program : Declarations Body'
    p[0] = p[1] + "START\n" + p[0] + "STOP\n"


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
    'Declaration: ARRAY LBRACKET NUM RBRACKET NAME DOTCOMMA'
    if p[5] not in p.parser.fp:
        p.parser.fp.update({p[5]: (p.parser.gp, int(p[3]))})
        p[0] = "PUSHN {p[3]}\n"
        p.parser.gp += int(p[3])
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[5]} already declared!")
        raise SyntaxError


def p_Declaration_Matrix(p):
    'Declaration: MATRIX LBRACKET NUM RBRACKET LBRACKET NUM RBRACKET NAME DOTCOMMA'
    if p[8] not in p.parser.fp:
        p.parser.fp.update({p[8]: (p.parser.gp, int(p[3]), int(p[6]))})
        n = int(p[3]) * int(p[6])
        p[0] = "PUSHN {str(n)}\n"
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
    'Assignment : NAME ATRIB Expr'
    if p[1] in p.parser.fp:
        p[0] = p[3] + f'STOREG {p.parser.fp.get(p[1])}\n'
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
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError


def p_Assignment_Matrix(p):
    'Assignment : NAME LBRACKET Expr RBRACKET LBRACKET Expr RBRACKET ATRIB Expr'
    if p[1] in p.parser.fp:
        var = p.parser.fp.get(p[1])
        if len(var) == 3:
            p[0] = f'PUSHGP\nPUSHI {var[0]}\nPADD\n{p[3]}PUSHI {var[2]}\nMUL\n{p[6]}ADD\n{p[9]}STOREN\n'
    else:
        print(f"Error, line {p.lineno(2)}: variable {p[1]} does not exists!")
        raise SyntaxError



    

#to build the parser call yacc.yacc()
parser = yacc.yacc()
#stack pointer aponta para o topo da stack
parser.sp
#frame pointer aponta para o endereço de base das vars locais
parser.fp = {}
#contem o endereço de base das vars locais
parser.gp = 0
#aponta para a instrução corrente por executar
parser.pc

parser.labels = 0