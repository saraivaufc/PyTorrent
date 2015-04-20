import part
import hashlib, os, pickle
from threading import Thread
import multiprocessing

chunk = 1024 * 512

class File(object):
	"""docstring for File"""
	__path = None
	__hash = None
	__parts = None

	def __init__(self, path = None):
		self.__path = path
		self.__parts = []
		self.__hash = self.get_hash_disk()
		self.load()

	def __eq__(self, part):
		return self.__hash == part.__hash

	#SETS
	def set_path(self, part):
		self.__path = part
	def set_hash(self, hash):
		self.__hash = hash

	#GETS
	def get_path(self):
		return self.__path
	def get_hash(self):
		return self.__hash
	def get_parts(self):
		self.load()
		return self.__parts
	def get_hash_disk(self):
		BLOCKSIZE = 65536
		hasher = hashlib.md5()
		try:
			with open(self.__path, 'rb') as afile:
				buf = afile.read(BLOCKSIZE)
				while len(buf) > 0:
					hasher.update(buf)
					buf = afile.read(BLOCKSIZE)
			return hasher.hexdigest()
		except:
			return None
	def get_parts_not_found(self):
		self.load()
		not_found = []
		for part in self.__parts:
			array = part.to_array()
			if array == None:
				not_found.append(part)
		return not_found

	def data_to_part(self, data):
		hash_data = hashlib.md5(data).hexdigest()
		part_file = part.Part(hash_data, str(self.__hash) + "/")
		try:
			os.mkdir(str(self.__hash) + "/")
		except:
			pass
		part_file.set_data(data)

	def part_to_data_in_parts(self, hash):
		part_file = part.Part(hash)
		data = None
		for i in self.__parts:
			if i == part_file:
				data = i.to_array()
		if data == None:
			data = self.part_to_data_in_file(hash)
		return data

	def part_to_data_in_file(self, hash):
		part_file = part.Part(hash)
		for i in self.__parts:
			if i == part_file:
				try:
					file = open(self.__path, "rb")
				except:
					return self.part_to_data_in_parts(hash)
				file.seek(i.get_index() - chunk)
				data_file = file.read(chunk)
				file.close()
				return data_file



	def merge(self):
		not_found = self.get_parts_not_found()
		if len(not_found) > 0:
			return False
		file = open(self.__path + ".copy", "wb")
		for part in self.__parts:
			array = part.to_array()
			file.write(array)
		file.close()
		if self.checksum():
			return True
		else:
			return False

	def checksum(self):
		return self.__hash == self.get_hash_disk()

	def load(self):
		try:
			dict_data = pickle.load( open( self.__path + ".pytorrent") )
		except:
			try:
				dict_data = pickle.load( open(self.__path) )
			except:
				return False
		self.__hash = dict_data['hash']
		self.__path = dict_data['path']
		self.__parts = dict_data['parts']
		return True
	def divider_parts(self):
		try:
			file = open(self.__path, "rb")
		except:
			print "Arquivo Not Founf"
			return False
		file.seek(0, 2)
		size_file = file.tell()
		file.seek(0)
		while file.tell() < size_file:
			buffer = file.read(chunk)
			part_file = part.Part(hashlib.md5(buffer).hexdigest(),str(self.__hash) + "/", file.tell())
			self.__parts.append(part_file)
		self.export()

	def export(self):
		dict_data = {'hash':self.__hash , 'path': self.__path , 'parts': self.__parts }
		string = pickle.dump(dict_data, open( self.__path + ".pytorrent" , "wb" ))

		
class CreatorSegment(Thread):
	"""docstring for CreatorSegment"""
	def __init__(self):
		Thread.__init__(self)

	def run(self, file, ):
		pass

		


# #f = File('ubuntu-12.04.5-desktop-i386.iso')
f = File('Raimundos  mulher de fases.mp3')
f.divider_parts()
# #print f.part_to_data_in_file("6a81a2f1b03c16207509ec5356dfa684")
# #print f.part_to_data_in_parts("6a81a2f1b03c16207509ec5356dfa684")
