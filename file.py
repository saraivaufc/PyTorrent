#-*- encoding=utf-8 -*-

import part, utils
import hashlib,json
import os.path

#chunk = 569344
chunk = 50000

class File(object):
	"""docstring for File"""
	__path = None
	__hash = None
	__parts = None
	__is_load = False

	def __init__(self, path = None):
		self.__path = path
		self.__parts = {}
		self.__hash = self.get_hash_disk()
		self.load()

	def __eq__(self, part):
		return self.__hash == part.__hash

	#SETS
	def set_path(self, part):
		self.__path = part
	def set_hash(self, new_hash):
		self.__hash = new_hash

	#GETS
	def get_path(self):
		return self.__path
	def get_hash(self):
		return self.__hash
	def get_parts(self):
		self.load()
		return self.__parts
	def get_hash_disk(self):
		if os.path.exists(self.__path):
			return utils.hash_for_file(self.__path)
		else:
			return None

	def get_parts_not_found(self):
		self.load()
		not_found = []
		for part in self.__parts.values():
			data = part.get_data()
			hash_part = utils.hash_for_string(data)
			if data == None or part.get_hash() != hash_part:
				not_found.append(part)
		return not_found

	def data_to_part(self, data):
		hash_data =  utils.hash_for_string(data)
		part_file = part.Part(hash_data, str(self.__hash) + "/")
		try:
			os.mkdir(str(self.__hash) + "/")
		except:
			pass
		part_file.set_data(data)

	def part_to_data_in_parts(self, hash_part, dead= False):
		try:
			part = self.__parts[hash_part]
		except:
			print "Parts NOT FOUNT in Parts"
			return self.part_to_data_in_file(hash_part, True)
		
		data = part.get_data()
		if data == None or len(data) <= 1:
			if dead == True:
				return None
			return self.part_to_data_in_file(hash_part, True)
		print "A part veio das Parts"
		return data

	def part_to_data_in_file(self, hash_part, dead= False):
		try:
			part = self.__parts[hash_part]
		except:
			print "Part NOT FOUND in File"
			return None
		try:
			f = open(self.__path, "rb")
		except:
			if dead == True:
				return None
			return self.part_to_data_in_parts(hash_part, True)
		f.seek(part.get_index() - chunk)
		data_file = f.read(chunk)
		f.close()
		print "A part veio do arquivo"
		return data_file

		#-------- **** -------


	def merge(self):
		self.load()
		print "Fazendo o merge do arquivos"
		not_found = self.get_parts_not_found()
		if len(not_found) > 0:
			return False
		f = open(self.__path, "wb")
		print "Foi encontradas " + str(len(self.__parts)) + "No diretorio"
		parts = self.__parts.values()
		parts.sort()
		print (parts)
		print "Asdsd"
		for part in parts:
			f.write(part.get_data())
		f.close()
		if self.checksum():
			return True
		else:
			return False

	def checksum(self):
		return self.__hash == self.get_hash_disk()

	def load(self):
		if self.__is_load:
			return
		else:
			self.__is_load = True

		print "Carregando o Arquivo: " + self.__path
		try:
			dict_data = json.loads( open(self.__path + ".pytorrent").read())
			print ".pytorrent FOUND"
		except:
			try:
				dict_data = json.loads( open(self.__path).read())
				print ".pytorrent FOUND"
			except:
				print ".pytorrent NOT FOUND"
				try:
					if os.path.exists(self.__path):
						self.divider_parts()
						self.__is_load = False
						return self.load()
					else:
						return False
				except:
					return False

		self.__hash = dict_data['hash']
		self.__path = dict_data['path']
		parts_str = json.loads(dict_data['parts'])
		self.__parts = {}
		for i in parts_str["parts"]:
			self.__parts[i["hash"]] = part.Part(i["hash"], self.__hash + "/" , i["index"])

		return True
	def divider_parts(self):
		print "Iniciando Particionamento"
		try:
			f = open(self.__path, "rb")
		except:
			print "Arquivo Not Founf"
			return False
		f.seek(0, 2)
		size_file = f.tell()
		f.seek(0)
		self.__parts = {}
		while f.tell() < size_file:
			buffer_size = f.read(chunk)
			hash_part = hashlib.md5(buffer_size).hexdigest()
			part_file = part.Part(hash_part,str(self.__hash) + "/", f.tell())
			part_file.set_data(buffer_size)
			self.__parts[hash_part] = part_file
		self.export()
		print "Terminou o particionamento"

	def export(self):
		json_parts = '{"parts" : ['
		is_fisrt = True
		print "Export parts " + str(len(self.__parts))
		for i in self.__parts.values():
			if is_fisrt:
				is_fisrt = False
			else:
				json_parts += ','
			json_parts += str(i.to_json())

		json_parts += "]}"
		dict_data = {'hash': self.__hash , 'path': self.__path , 'parts': str(json_parts) }
		json.dump(dict_data, open( self.__path + ".pytorrent" , "wb" ))

	def is_complete(self):
		self.load()
		for i in self.__parts.values():
			if i.exist() == False:
				return False
		return True
	
	def exist(self):
		self.load()
		try:
			if self.get_hash() == self.get_hash_disk():
				return True
		except:
			return False


