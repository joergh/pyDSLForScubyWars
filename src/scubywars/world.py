'''
Created on Feb 18, 2012

@author: jh
'''

from scubywars import dummy
from mathlib import *
import time
import math

class player():
    def __init__(self, message):
        self.msg = message
    
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
    
def update(enemy):
    global _server
    id = enemy.get_id()
    for p in _server.get_players():
        pl = player(p)
        if pl.get_id() == id:
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
