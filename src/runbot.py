'''
Created on Feb 18, 2012

@author: jh
'''

import parser

from scubywars import swapi, world, bot

if __name__ == '__main__':
    host = '10.1.1.19'
    #host = 'localhost'
    server = swapi.swconn(host, 1337, swapi.PLAYERTYPE_PLAYER, "JOE_DSL1")
    server.connect()
    world.set_server(server)
    bot.set_server(server)

    parser.do_generate("test.sb1", debug=True)
    botcode = __import__("botcode")
    botcode.run_bot()