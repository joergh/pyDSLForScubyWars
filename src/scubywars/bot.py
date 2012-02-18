'''
Created on Feb 18, 2012

@author: jh
'''

_thrust = False
_left = False
_right = False
_fire = False

def set_server(server):
    global _server
    _server = server

def can_fire():
    global _server
    return _server.get_has_shot()

def view_angle():
    global _server
    return _server.get_dir()

def position():
    global _server
    return _server.get_pos()

def turn_to(obj):
    global _server
    if obj.get_signed_angle() < 0.0:
        turn_right()
    else:
        turn_left()
    
def turn_left():
    global _left
    _left = True

def turn_right():
    global _right
    _right = True

def thrust():
    global _thrust
    _thrust = True
    
def fire():
    global _fire
    _fire = True

def action():
    global _left, _right, _thrust, _fire
    _server.do(_left, _right, _thrust, _fire)
    _left, _right, _thrust, _fire = (False, False, False, False)