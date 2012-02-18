'''
Created on Feb 17, 2012

@author: jh
'''

from ply import lex

reserved = {
   'if' : 'IF',
   'can' : 'CAN',
   'find' : 'FIND',
   'min' : 'MIN',
   'max' : 'MAX',
   'is'  : 'IS',
   'thrust' : 'THRUST', 
   'turn' : 'TURN',
   'to'   : 'TO',
   'left' : 'LEFT',
   'right' : 'RIGHT',
   'fire' : 'FIRE',
   'state' : 'STATE',
   'distance' : 'DIST',
   'angle' : 'ANGLE',
   'and' : 'AND',
   'or' : 'OR',
   'enemy' : 'ENEMY',
   'ship' : 'SHIP',
   'shot' : 'SHOT',
   'dead' : 'DEAD',
   'end' : 'END',
}

def t_WORD(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'WORD')    # Check for reserved words
    return t

tokens = [
   'NEWLINE',
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'ASSIGN',
   'COMMENT',
   'EQUAL',
   'LT',
   'GT',
   'GE',
   'LE',
   'STATEDEF',
   'WORD',
] + reserved.values()

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ASSIGN  = r'\='
t_LT      = r'\<'
t_GT      = r'\>'
t_LE      = r'\<='
t_GE      = r'\>='
t_EQUAL   = r'\=='
t_STATEDEF= r'\:\:'


    
def t_NUMBER(t):
    r'[-+]?[0-9]*\.?[0-9]+'
    t.value = float(t.value)    
    return t
    
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()
