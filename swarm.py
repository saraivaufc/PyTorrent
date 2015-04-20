class Swarm(object):
	"""docstring for Swarm"""
	__hash_file = None
	__part_peer = None

	def __init__(self, hash_file = None):
		self.__hash_file = hash_file
		self.__part_peer = {}

	def __eq__(self, swarm):
		return self.__hash_file == swarm.__hash_file

	def set_hash_file(self, hash_file):
		self.__hash_file = hash_file
	def get_hash_file(self):
		return self.__hash_file

	def get_peers(self, hash_part):
		try:
			return self.__part_peer[hash_part].get_peers()
		except:
			return []
				
	def get_peers_better(self, hash_part):
		try:
			return self.__part_peer[hash_part].get_peers_better()
		except:
			return []
	def get_part_peer(self, hash_part):
		try:
			return self.__part_peer[hash_part]
		except:
			return []

	def add_peer(self, hash_part, peer):
		try:
			self.__part_peer[hash_part].add_peer(peer)
		except:
			self.__part_peer[hash_part] = PartPeer(hash_part)
			self.add_peer(hash_part, peer)


	def remove_peer(self, hash_part, peer):
		try:
			self.__part_peer[hash_part].remove_peer(peer)
		except:
			return
	def update_peers(self):
		pass

class PartPeer():
	__hash_part = None
	__peers = None

	def  __init__(self, hash_part):
		self.__hash_part = hash_part
		self.__peers = []

	def get_hash_part(self):
		return self.__hash_part

	def add_peer(self, peer):
		if peer in self.__peers:
			return
		else:
			self.__peers.append(peer)

	def remove_peer(self, peer):
		self.__peers.remove(peer)

	def get_peers(self):
		return self.__peers

	def get_peers_better(self):
		return self.__peers[:4]