import address, swarm, peer

from socket import *
from threading import Thread
import json


chunk = 1024 * 10

class Tracker():
	"""docstring for Tracker"""

	__address = None
	__swarms = None
	__seeds_alive = None
	__socket_tracker = None

	def __init__(self, address = None):
		self.__address = address
		self.__swarms = {}
		self.__seeds_alive = []

	def __eq__(self, tracker):
		return self.__address == tracker.__address

	def run(self):
		self.__socket_tracker = socket(AF_INET, SOCK_DGRAM)
		self.__socket_tracker.bind((self.__address.get_ip(),self.__address.get_port()))
		while 1:
			message, client_address = self.__socket_tracker.recvfrom(chunk)
			print "Tracker : Pergunta Recebida de " + str(client_address) + " no endereco:" + str(self.__address)
			th=Thread( target=self.treat_request_thread,
						args = ( client_address, message))
			th.start()
		self.__socket_tracker.close()


	def set_address(self, address):
		self.__address = address
	def get_address(self):
		return self.__address


	def add_peer_in_swarm(self, hash_file, hash_part, address):
		th=Thread( target=self.add_peer_in_swarm_thread,
					args = ( hash_file, hash_part, address, ) )
		th.start()
	def add_peer_in_swarm_thread(self, hash_file, hash_part, address):
		try:
			swarm_file = self.__swarms[hash_file]
			swarm_file.add_peer(hash_part, peer.Peer(address, [self,]))
		except:
			swarm_file = swarm.Swarm(hash_file)
			swarm_file.add_peer(hash_part, peer.Peer(address, [self,]))
			self.__swarms[hash_file] = swarm_file


	def rem_peer_in_swarm(self, hash_file, hash_part, address):
		th=Thread( target=self.rem_peer_in_swarm_thread,
					args = (hash_file, hash_part, address, ) )
		th.start()
	def rem_peer_in_swarm_thread(self, hash_file,hash_part, address):
		try:
			swarm_file = self.__swarms[hash_file]
			swarm_file.remove_peer(hash_part, peer.Peer(address, [self,]))
		except:
			return

	def get_peers_swarm(self, hash_file, hash_part):
		try:
			return self.__swarms[hash_file].get_peers(hash_part)
		except:
			return None


	def treat_request_thread(self, address, request):
		request = json.loads(str(request))
		response = ""
		type_request = int(request["type"])
		if type_request == 1:
			if  not (address.get_ip() in self.__seeds_alive): 
				self.__seeds_alive.append(address.get_ip())
			response = json.dumps({"type": 10})
		elif type_request == 2:
			hash_file = request["file"]
			hash_part = request["part"]
			self.add_peer_in_swarm(hash_file, hash_part, address)
			response = json.dumps({"type": 20})
		elif type_request == 3:
			hash_file = request["file"]
			hash_part = request["part"]
			try:
				swarm_file = self.__swarms[hash_file]
				peers = swarm_file.get_peers(hash_part)
				address_peers = []
				for i in peers:
					address_peers.append(i.get_address())
				print address_peers
				response = json.dumps({"type": 30 , "address_peers": address_peers }) #"swarm": swarm_file
			except:
				response = "Erro"
				print "Hash File not found"
		self.__socket_tracker.sendto(response, address)
		print "Tracker : Resposta Enviada a " + str(address) + " por " + str(self.__address)

#nc -u localhost 8000
