'''
Created on Feb 18, 2012

@author: jh
'''

class bot:
    def __init__(self, server):
        self.thr = False
        self.lft = False
        self.rght = False
        self.fr = False
        self.server = server
        
    def can_fire(self):
        return self.server.get_has_shot()
    
    def view_angle(self):
        return self.server.get_dir()
    
    def position(self):
        return self.server.get_pos()
    
    def turn_to(self, obj):
        if obj.get_signed_angle() < 0.0:
            self.turn_right()
        else:
            self.turn_left()
        
    def turn_left(self):
        self.lft = True
    
    def turn_right(self):
        self.rght = True
    
    def thrust(self):
        self.thr = True
        
    def fire(self):
        self.fr = True
    
    def action(self):
        self.server.do(self.lft, self.rght, self.thr, self.fr)
        self.lft, self.rght, self.thr, self.fr = (False, False, False, False)