'''
Created on Feb 17, 2012

@author: jh
'''

from ply import yacc
import tokendef
import sys

from definitions import preamble, postamble

tokens = tokendef.tokens

_starting_state = None

precedence = (
    ('left', 'GT', 'LT', 'LE', 'GE', 'EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def _emit_debug(p, line):
    if debug_mode:
        _emit(p, 'print "{}"'.format(line))

def _emit_action(p, line):
    _emit(p, line)
    if debug_mode:
        _emit(p, 'print "{}"'.format(line))
    
def _emit(p, line):
    for i in range(p.parser.indent + 1):
        p.parser.out.write("    ")
    p.parser.out.write(line)
    p.parser.out.write('\n')

def p_program(p):
    '''program : program statement
               | statement'''

def p_statement_end(p):
    '''statement : END
                 | NEWLINE'''
    _emit(p, "")
    if p.parser.indent > 1:
        p.parser.indent -= 1
          
def p_statement(p):
    '''statement : assignment
                 | formdef
                 | statechange
                 | statedef
                 | if
                 | find
                 | action'''

def p_statement_store(p):
    '''statement : STORE WORD NEWLINE'''
    _emit(p, "self.{} = self.enemy".format(p[2]))

def p_statement_recall(p):
    '''statement : RECALL WORD NEWLINE'''
    _emit(p, "self.enemy = self.{}".format(p[2]))
    
def p_action(p):
    '''action : FIRE
              | TURN LEFT
              | TURN RIGHT
              | THRUST'''
    if len(p) == 2:
        func = str(p[1])
    else:
        func = "{}_{}".format(p[1], p[2])
    _emit_action(p, "self.bot.{}()".format(func))
    
def p_action_turn_to(p):
    '''action : TURN TO'''
    func = "{}_{}".format(p[1], p[2])
    _emit_action(p, "self.bot.{}(enemy)".format(func))
    
def p_statedef(p):
    '''statedef : WORD STATEDEF NEWLINE'''
    global _starting_state
    p.parser.indent = 0
    _emit(p, "def {}(self):".format(p[1]))
    if not _starting_state:
        _starting_state = p[1]
    p.parser.indent = 1
    _emit(p, "enemy = self.enemy")
    _emit_debug(p, "STATE: {}".format(p[1]))

def p_statechange(p):
    '''statechange : STATE WORD NEWLINE'''
    _emit(p, "self.current_state = self.{}".format(p[2]))
    _emit_action(p, "return")
    
def p_assignment(p):
    '''assignment : WORD ASSIGN expression NEWLINE'''
    _emit(p, "self.{} = {}".format(p[1], p[3]))
    
def p_formdef(p):
    '''formdef : WORD FORMDEF expression NEWLINE'''
    indent = p.parser.indent
    p.parser.indent = 0
    _emit(p, "def {}(self, enemy):".format(p[1]))
    p.parser.indent += 1
    _emit(p, "val = {}".format(p[3]))
    if debug_mode:
        _emit(p, "print '{} := ' + str(val)".format(p[1]))
    _emit(p, "return val")
    p.parser.indent = indent
    
def p_if(p):
    '''if : IF boolean NEWLINE'''
    _emit(p,"if {}:".format(p[2]))
    p.parser.indent += 1

def p_boolean_not(p):
    '''boolean : NOT boolean'''
    p[0] = 'not {}'.format(p[2])
    
def p_boolean_is(p):
    '''boolean : IS SHIP
               | IS SHOT
               | IS ENEMY
               | IS TARGETED
               | IS DUMMY
               | IS DEAD'''
    p[0] = "enemy.is_{}()".format(p[2])
    
def p_boolean_can(p):
    '''boolean : CAN FIRE'''
    p[0] = "self.bot.can_{}()".format(p[2])
    
def p_boolean_binop(p):
    '''boolean : boolean AND boolean
               | boolean OR boolean'''
    p[0] = "{} {} {}".format(p[1], p[2], p[3])
    
def p_boolean_bracket(p):
    '''boolean : LPAREN boolean RPAREN'''
    p[0] = "(" + str(p[2]) + ")"

def p_find(p):
    '''find : FIND MIN expression NEWLINE
            | FIND MAX expression NEWLINE'''
    _emit(p, "try:")
    p.parser.indent += 1
    _emit(p, "_obj_list = self.world.get_objects()")
    _emit(p, "_obj_list = [ (enemy, {}) for enemy in _obj_list ]".format(p[3]))
    _emit(p, "enemy, _val = reduce (_filter_find_{}, _obj_list)".format(p[2]))
    p.parser.indent -= 1
    _emit(p, "except Exception as e:")
    p.parser.indent += 1
    _emit(p,"enemy = dummy()")
    p.parser.indent -= 1
    _emit_debug(p,'Selected Enemy: " + str(self.enemy) + "')
    _emit(p, "self.enemy = enemy")
        
def p_find_filter(p):
    '''find : FIND MIN expression AND boolean NEWLINE'''
    boolexpr = p[5].replace('enemy.', 'enemy.')
    _emit(p, "try:")
    p.parser.indent += 1
    _emit(p, "_obj_list = self.world.get_objects()")
    _emit(p, "_obj_list = [ (enemy, {}) for enemy in _obj_list ]".format(boolexpr))
    _emit(p, "_obj_list = filter (_is_filter_valid, _obj_list)".format(boolexpr))
    _emit(p, "_obj_list = [ (enemy, {}) for (enemy, bool) in _obj_list ]".format(p[3]))
    _emit(p, "enemy, _val = reduce (_filter_find_{}, _obj_list)".format(p[2]))
    p.parser.indent -= 1
    _emit(p, "except Exception as e:")
    p.parser.indent += 1
    _emit(p,"enemy = dummy()")
    p.parser.indent -= 1
    _emit_debug(p,'Selected Enemy: " + str(self.enemy) + "')
    _emit(p, "self.enemy = enemy")
    
def p_boolean_comp(p):
    '''boolean : expression LT expression
               | expression GT expression
               | expression LE expression
               | expression GE expression
               | expression EQUAL expression'''
    p[0] = "{} {} {}".format(p[1], p[2], p[3])
    
def p_expression_binop(p):
    '''expression : expression PLUS expression
           | expression MINUS expression
           | expression TIMES expression
           | expression DIVIDE expression'''
    p[0] = "{} {} {}".format(p[1], p[2], p[3])

def p_expression_paren(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = "({})".format(p[2])

def p_expression_bracket(p):
    '''expression : LBRACKET expression RBRACKET'''
    p[0] = "{}(enemy)".format(p[2])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = str(p[1])

def p_expression_var(p):
    '''expression : WORD'''
    p[0] = "self.{}".format(p[1])

def p_expression_enemy(p):
    '''expression : DIST
                  | ANGLE'''
    p[0] = "enemy.get_{}()".format(p[1])

def p_error(t): 
    print("------------- Syntax error in line %d at '%s'" % (t.lexer.lineno, t.value)) 

def do_generate(source, debug=False):
    global debug_mode
    debug_mode = debug
    parser = yacc.yacc()
    parser.indent = 1
    parser.out = open("botcode.py", "w")
    parser.out.write(preamble)
    parser.parse(open(source).read(), debug=False)
    parser.out.write(postamble.format(_starting_state))
    parser.out.close()
    
if __name__ == '__main__':
    do_generate(sys.argv[1])