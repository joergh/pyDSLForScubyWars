'''
Created on Feb 18, 2012

@author: jh
'''

preamble = '''
# some simple helpers
from scubywars import world, bot, dummy
from time import sleep

enemy = dummy()

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
'''

postamble='''

_current_state = {}

def run_bot():
    global enemy
    
    while True:
        enemy = world.update(enemy)
        _current_state()
        bot.action()
        world.wait_next()
'''