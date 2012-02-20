'''
Created on Feb 18, 2012

@author: jh
'''

import parser

from scubywars import swapi, world, bot

if __name__ == '__main__':
    num_bots = 1
    host = '10.1.1.183'
    #host = 'localhost'
    server = swapi.swconn(host, 1337, swapi.PLAYERTYPE_PLAYER, "JOE_DSL_EVO")
    server.connect()
    world.set_server(server)
    bot.set_server(server)

    
    parser.do_generate("test.sb1", debug=True)
    botcode = __import__("botcode")
    for i in range(num_bots):
        bot = botcode.bot_impl()
        bot.start()