import hashlib, os
import json

class Part():
	"""docstring for Part"""
	__hash = None
	__path = None
	__index = None

	def __init__(self, hash = None, dir  = None, index = None):
		self.__hash = hash
		self.__path = str(dir) + str(hash) + ".part"
		self.__index = index
		self.create_dir(dir)
	def __eq__(self, part):
		return self.__hash == part.__hash

	def to_JSON(self):
		return str(json.dumps({"hash": self.__hash, "path": self.__path, "index": self.__index})).encode("utf_8")
		
	def create_dir(self, dir):
		try:
			os.mkdir(dir)
		except:
			pass

	def set_hash(self, hash):
		self.__hash = hash
	def set_path(self, path):
		self.__path = path
	def set_data(self, data):
		try:
			import os.path
			if os.path.exists(self.__path):
				print "Part found"
				return
			file = open(self.__path, "wb")
			file.write(data)
			file.close()
		except:
			print "IOError"


	def get_hash(self):
		return self.__hash
	def get_hash_disk(self):
		try:
			data = self.get_data()
			return hashlib.md5(data).hexdigest()
		except:
			return None	
	def get_path(self):
		return self.__path
	def get_index(self):
		return self.__index
		
	def get_data(self):
		try:
			return open(self.__path, "rb").read()
		except:
			return None

	def checksum(self):
		return self.__hash == self.get_hash_disk()

	def to_array(self):
		try:
			data = open(self.__path, "rb").read()
		except:
			print "Erro IO - to_array"
			return None
		if hashlib.md5(data).hexdigest() != self.__hash:
			print "Erro no Ckecksum da Part"
			return None
		return data

	def exist(self):
		try:
			data = open(self.__path, "rb").read()
			return  hashlib.md5(data).hexdigest() == self.__hash
		except:
			print "checksum --> PART NOT FOUND"
			return False
