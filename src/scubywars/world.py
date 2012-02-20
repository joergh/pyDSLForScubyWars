'''
Created on Feb 18, 2012

@author: jh
'''

from scubywars import dummy, mathlib
from mathlib import *
import time
import math

class player():
    def __init__(self, message):
        self.msg = message
        self.vector=(0.0,0.0)
        
    def set_vector(self, x, y):
        self.vector = (x,y)
        
    def get_position(self):
        return (self.msg[1], self.msg[2])
    
    def get_distance(self):
        global _server
        x, y = _server.get_pos()
        return dist(x, y, self.msg[1], self.msg[2])
    
    def get_signed_angle(self):
        global _server
        x, y = _server.get_pos()
        dirvec = rot(1.0, 0.0, _server.get_dir())
        return anglediff(x, y, self.msg[1], self.msg[2], dirvec[0], dirvec[1])
    
    def get_angle(self):
        return math.fabs(self.get_signed_angle())

    def is_enemy(self):
        global _server
        #return True
        return not _server.is_myplayer(self.msg[0])
    
    def is_targeted(self):
        global _server
        for pl in get_objects():
            if not pl.is_enemy():
                x, y = pl.get_position()
                dirvec = rot(1.0, 0.0, pl.get_signed_angle())
                if mathlib.anglediff(x, y, self.msg[1], self.msg[2], dirvec[0], dirvec[1]) < 0.3:
                    print "{} is targeted by {}".format(self.get_name(), pl.get_name())
                    return True
        return False
                
    def is_shot(self):
        global _server
        return False

    def is_ship(self):
        global _server
        return True

    def is_dead(self):
        global _server
        return False
        
    def get_id(self):
        global _server
        return str(self.msg[0])
    
    def get_name(self):
        global _server
        return _server.get_playername(self.msg[0])
    
    def is_dummy(self):
        return False
        
def update(enemy):
    global _server
    id = enemy.get_id()
    for p in _server.get_players():
        pl = player(p)
        if pl.get_id() == id:
            pl.set_vector(enemy.msg[1] - pl.msg[1], enemy.msg[2] - pl.msg[2])
            return pl
    return dummy()
    
def set_server(server):
    global _server
    _server = server
    
def get_objects():
    global _server
    return map(player, _server.get_players())

_last_round = -1

def wait_next():
    global _server, _last_round
    
    while _server.get_round() == _last_round:
        time.sleep(0.001)
    _last_round = _server.get_round()
