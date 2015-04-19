class Swarm(object):
	"""docstring for Swarm"""
	__hash = None
	__peers = None

	def __init__(self, hash = None, peers = []):
		self.__hash = hash
		self.__peers = peers

	def __eq__(self, swarm):
		return self.__hash == swarm.__hash

	def set_hash(self, hash):
		self.__hash = hash
	def get_hash(self):
		return self.__hash

	def get_peers(self):
		return self.__peers
	def add_peer(self, peer):
		self.__peers.append(peer)
	def rem_peer(self, peer):
		self.__peers.remove(peer)
	def update_peers(self):
		pass
	def get_peers_better(self):
		pass
		