class Swarm(object):
	"""docstring for Swarm"""
	__hash_file = None
	__peers = None

	def __init__(self, hash_file = None):
		self.__hash_file = hash_file
		self.__peers = []

	def __eq__(self, swarm):
		return self.__hash_file == swarm.__hash_file

	def set_hash_file(self, hash_file):
		self.__hash_file = hash_file
	def get_hash_file(self):
		return self.__hash_file
	
	def get_peers_ordering(self):
		""" Ainda tenho que ordenar essa daqui """
		return self.__peers
	def get_peers(self):
		return self.__peers

	def add_peer(self, peer):
		try:
			self.__peers.append(peer)
			return True
		except:
			return False

	def remove_peer(self, peer):
		try:
			self.__peers.remove(peer)
		except:
			return
	def update_peers(self):
		pass