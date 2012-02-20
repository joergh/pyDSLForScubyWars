'''
Created on Feb 18, 2012

@author: jh
'''

from scubywars import dummy, mathlib
from mathlib import *
import time
import math

class player():
    def __init__(self, message, server):
        self.server = server
        self.msg = message
        self.vector=(0.0,0.0)
        
    def set_vector(self, x, y):
        self.vector = (x,y)
        
    def get_position(self):
        return (self.msg[1], self.msg[2])
    
    def get_distance(self):
        x, y = self.server.get_pos()
        return dist(x, y, self.msg[1], self.msg[2])
    
    def get_signed_angle(self):
        x, y = self.server.get_pos()
        dirvec = rot(1.0, 0.0, self.server.get_dir())
        return anglediff(x, y, self.msg[1], self.msg[2], dirvec[0], dirvec[1])
    
    def get_angle(self):
        return math.fabs(self.get_signed_angle())

    def is_enemy(self):
        return not self.server.is_myplayer(self.msg[0])
    
    def is_targeted(self):
        for pl in get_objects():
            if not pl.is_enemy():
                x, y = pl.get_position()
                dirvec = rot(1.0, 0.0, pl.get_signed_angle())
                if mathlib.anglediff(x, y, self.msg[1], self.msg[2], dirvec[0], dirvec[1]) < 0.3:
                    print "{} is targeted by {}".format(self.get_name(), pl.get_name())
                    return True
        return False
                
    def is_shot(self):
        return False

    def is_ship(self):
        return True

    def is_dead(self):
        return False
        
    def get_id(self):
        return str(self.msg[0])
    
    def get_name(self):
        return self.server.get_playername(self.msg[0])
    
    def is_dummy(self):
        return False
        
class world:
    def __init__(self, server):
        self.server = server
        self.last_round = -1
        
    def update(self, enemy):
        id = enemy.get_id()
        for p in self.server.get_players():
            pl = player(p, self.server)
            if pl.get_id() == id:
                pl.set_vector(enemy.msg[1] - pl.msg[1], enemy.msg[2] - pl.msg[2])
                return pl
        return dummy()
        
    def get_objects(self):
        return [ player(p, self.server) for p in self.server.get_players() ]
    
    def wait_next(self):
        try:
            last_round = self.last_round
        except:
            last_round = -1
                    
        while self.server.get_round() == last_round:
            time.sleep(0.001)
        self.last_round = self.server.get_round()
