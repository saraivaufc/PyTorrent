class Address():
	"""docstring for Address"""
	__ip = None
	__port = None

	def __init__(self, ip = None, port = None):
		self.__ip = ip
		self.__port = port

	def __eq__(self, address):
		return self.__ip == address.__ip and self.__port == address.__port

	def set_ip(self, ip):
		self.__ip = ip

	def set_port(self, port):
		self.__port = port

	def get_ip(self):
		return self.__ip

	def get_port(self):
		return self.__port

