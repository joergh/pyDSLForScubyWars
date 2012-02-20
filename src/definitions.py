'''
Created on Feb 18, 2012

@author: jh
'''

preamble = '''
# some simple helpers
import threading
from scubywars import world, bot, dummy
from time import sleep

def _is_filter_valid(obj):
    enemy, bool = obj
    return bool

def _filter_find_min(obj1, obj2):
    enemy1, num1 = obj1
    enemy2, num2 = obj2
    
    if num1 < num2:
        return obj1
    else:
        return obj2
    
def _filter_find_max(obj1, obj2):
    enemy1, num1 = obj1
    enemy2, num2 = obj2
    
    if num1 > num2:
        return obj1
    else:
        return obj2

# compiled states start here
class bot_impl(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.enemy = dummy()
        current_state = None
        self.server = server
        self.world = world.world(server)
        self.bot = bot.bot(server)
        
    def startup(self):
'''

postamble='''
    def run(self):
        self.current_state = self.{}
        self.startup()
        while True:
            self.enemy = self.world.update(self.enemy)
            self.current_state()
            self.bot.action()
            self.world.wait_next()
'''