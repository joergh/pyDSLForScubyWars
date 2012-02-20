'''
Created on Feb 18, 2012

@author: jh
'''

import parser

from scubywars import swapi, world, bot

if __name__ == '__main__':
    num_bots = 5
    host = '10.1.1.183'
    
    parser.do_generate("test.sb1", debug=True)
    botcode = __import__("botcode")
    for i in range(num_bots):
        server = swapi.swconn(host, 1337, swapi.PLAYERTYPE_PLAYER, "JOE_DSL_EVO")
        server.connect()
        bot = botcode.bot_impl(server)
        bot.start()