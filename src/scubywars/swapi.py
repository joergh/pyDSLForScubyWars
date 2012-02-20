import socket
from threading import Thread
from struct import pack, unpack
import sys
import pprint

MSGTYPE_PLAYER     = 0 #Server->Client
MSGTYPE_SHOT       = 1 #Server->Client
MSGTYPE_POWERUP    = 2 #Server->Client
MSGTYPE_WORLD      = 3 #Server->Client
MSGTYPE_HANDSHAKE  = 4 #Server<->Client
MSGTYPE_ACTION 	   = 5 #Client->Server
MSGTYPE_SCOREBOARD = 6 #Server->Client
MSGTYPE_PLAYERJOIN = 7 #Server->Client
MSGTYPE_PLAYERLEFT = 8 #Server->Client
MSGTYPE_PLAYERNAME = 9 #Server->Client

PLAYERTYPE_PLAYER = 0
PLAYERTYPE_LISTENER = 1

class message:
	type = MSGTYPE_HANDSHAKE
	content = []

	def get_data(self):
		return self.content
	
class message_handshake(message):
	def __init__(self, type, name):
		self.type = MSGTYPE_HANDSHAKE
		self.name = ""
		self.len = 2
		for c in name:
			self.name = self.name + "\0" + c
			self.len += 2 
		self.relationType = type
		
	def get_data(self):
		return pack('>hih', self.type, self.len, self.relationType) + self.name
		
class swconn:
	has_shot = False
	pos = (0,0)
	dir = 0
	
	myplayers = {}
	playernames = {}
	players = []
	
	def __init__(self, host, port, type, name):
		self.host = host
		self.port = port
		self.type = type
		self.name = name
		self.id = None
		self.round = 0
		
	def get_id(self):
		return id
	
	def get_name(self):
		return self.name
	
	def get_playername(self, id):
		try:
			return self.playernames[id]
		except:
			return '(--)'
		
	def is_myplayer(self, id):
		if self.myplayers.has_key(id):
			return True
		return False
		
	def get_dir(self):
		return self.dir
	
	def get_pos(self):
		return self.pos

	def get_has_shot(self):
		return self.has_shot
		
	def get_players(self):
		return self.players
	
	def get_round(self):
		return self.round
	
	def do(self, turn_left, turn_right, thrust, fire):
		self.sock.send(pack('>hibbbb', MSGTYPE_ACTION, 4, turn_left, turn_right, thrust, fire))
			
	def connect(self):
		self.sock = socket.create_connection((self.host, self.port), 10)
		self.sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
		
		self.sock.send(message_handshake(self.type, self.name).get_data())

		class msg_receiver(Thread):
			def __init__(self, rw, sock):
				Thread.__init__(self)
				self.rw = rw
				self.sock = sock
				self.players = []
				self.has_shot = True
				self.daemon = True
				
			def receive_all(self, size):
				buffer = ""
				while size > 0:
					buffer += self.sock.recv(size)
					size -= len(buffer)
				return buffer
			
			def read_message(self):
				header = self.receive_all(6)
				type, length = unpack('>hi', header)
				
				data = self.receive_all(length)

				if type == MSGTYPE_WORLD:
					self.rw.players = self.players
					self.players = []
					self.rw.has_shot = self.has_shot
					self.has_shot = True
					self.rw.round += 1
					
				elif type == MSGTYPE_HANDSHAKE:
					ack, self.rw.id = unpack('>bq', data)
					if ack != 0:
						print "Name already in use?!? Exiting!"
						sys.exit()
					print "Logged in with id: " + repr(self.rw.id)
				elif type == MSGTYPE_PLAYER:
					msg = unpack('>qfffhhfbbbb', data)
					if msg[0] == self.rw.id:
						self.rw.pos = (msg[1], msg[2])
						self.rw.dir = msg[3]
					else:
						self.players.append(msg)
						
				elif type == MSGTYPE_SHOT:
					msg = unpack('>qfffhhqf', data)
					if msg[6] == self.rw.id:
						self.has_shot = False
				elif type == MSGTYPE_PLAYERLEFT:
					msg = unpack('>q', data)
					try:
						del self.rw.myplayers[msg[0]]
						del self.rw.playernames[msg[0]]
					except:
						pass
				elif type in (MSGTYPE_PLAYERNAME, MSGTYPE_PLAYERJOIN):
					chars = (len(data) - 8) / 2
					msg = unpack('>q{}h'.format(chars), data)
					name = ""
					print 
					for char in msg[1:]:
						name += chr(char)
					self.rw.playernames[msg[0]] = name
					if name.startswith(self.rw.get_name()):
						self.rw.myplayers[msg[0]] = name
			def run(self):
				while True:
					msg = self.read_message()
					
		self.thread = msg_receiver(self, self.sock)
		self.thread.start()