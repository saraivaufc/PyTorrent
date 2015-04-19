import address
import swarm

class Tracker():
	"""docstring for Tracker"""

	__address = None
	__swarms = None
	__seeds_alive = None

	def __init__(self, address = None, swarms = [], seeds_alive = []):
		self.__address = address
		self.__swarms = swarms
		self.__seeds_alive = seeds_alive

	def __eq__(self, tracker):
		return self.__address == tracker.__address

	def set_address(self, address):
		self.__address = address
	def get_address(self):
		return self.__address

	def add_swarm(self, hash_file):
		pass
	def rem_swarm(self, hash_file):
		pass
	def get_swarm(self, hash_file):
		pass

	def waiting_connections(self, address):
		pass

	def  receive_part_seed(self):
		pass



