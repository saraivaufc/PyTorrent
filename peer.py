import  address
#import tracker
import leecher, seed, file
from socket import *
import pickle
from threading import Thread


class Peer():
	"""docstring for Peer"""
	__address = None
	__speed_download = None
	__speed_upload = None
	__trackers = None
	__files_upload = None
	__files_download = None

	def __init__(self, address = None, trackers = []):
		self.__address = address
		self.__speed_download = 0.0
		self.__speed_upload = 0.0
		self.__files_download = {}
		self.__files_upload = {}
		self.__trackers = trackers
	def __eq__(self, peer):
		return self.__address.get_ip() == peer.__address.get_ip()

	def run(self):
		client_socket = socket(AF_INET, SOCK_DGRAM)
		message = pickle.dumps({"type": 2, "file": "sdadsadsa", "part": "sdjad" })
		client_socket.sendto(message, ("127.0.0.1", 8000))
		print "Peer : Requiscao Enviada"
		message, tracker_address = client_socket.recvfrom(2084)
		print "Peer : Resposta Recebida == " + message
		client_socket.close()

	# Path references .pytorrent
	def download(self, path):
		th=Thread( target=self.download_thread,
					args = ( path, ) )
		th.start()
		
	def download_thread(self, path):
		f = file.File(path)
		hash_file = f.get_hash()
		self.__files_download[hash_file] = f
		client_socket = socket(AF_INET, SOCK_DGRAM)
		
		#para cada uma das partes
		for i in f.get_parts():
			hash_part = i.get_hash()
			message = pickle.dumps({"type":3, "file": hash_file, "part": hash_part })

			#para cada um dos trackers
			for k in self.__trackers:
				client_socket.sendto(message, (k.get_address().get_ip(),k.get_address().get_port()))
				print "Peer - Pergunta enviada"
			while 1:
				message, client_address = client_socket.recvfrom(2084)
				print "Peer - Resposta Recebida"
				try:
					message = pickle.loads(message)
					th=Thread( target=self.download_part_thread,
								args = ( hash_file,hash_part, message ) )
					th.start()
				except:
					print "Falha ao carregar a resposta"
	def download_part_thread(self, hash_file, hash_part, message):
		for i in message["address_peers"]:
			client_socket_download = socket(AF_INET, SOCK_DGRAM)
			msn = pickle.dumps({"type": 1,"file": hash_file, "part" : hash_part})
			client_socket_download.sendto(msn, i )
			th=Thread( target=self.download_part_peer,
								args = ( hash_file,hash_part, client_socket_download ) )
			th.start()

	def download_part_peer(self, hash_file, hash_part, socket_download):
		print "Heelo"
		message, client_address = socket_download.recvfrom(2084)
		print message




	def upload(self, path):
		th=Thread( target=self.upload_thread,
					args = ( path, ) )
		th.start()
	def upload_thread(self, path):
		f = file.File(path)
		self.__files_upload[f.get_hash()] = f
		f.divider_parts()
		client_socket = socket(AF_INET, SOCK_DGRAM)
		for i in f.get_parts():
			message = pickle.dumps({"type": 2, "file": f.get_hash(), "part": i.get_hash() })
			for k in self.__trackers:
				client_socket.sendto(message, (k.get_address().get_ip(),k.get_address().get_port()))
		while 1:
			message, client_address = client_socket.recvfrom(2084)
			message = pickle.loads(message)
			if int(message["type"]) == 1:
				th=Thread( target=self.upload_part_thread,
						args = ( message["file"], message["part"], client_address, client_socket))
				th.start()
		client_socket.close()

	def upload_part_thread(self,hash_file, hash_part, address, socket):
		response = ""
		try:
			f = self.__files_upload[hash_file]
			data = f.part_to_data_in_parts()
			response = pickle.dumps({"type": 10, "hash": hash_file, "part": hash_part, "data": data })
		except:
			pass
		socket.sendto(response, address)
		print "Enviado Part para o Peer que requisitou"





	def set_address(self, address):
		self.__address = address
	def  get_address(self):
		return self.__address

	def get_speed_download(self):
		return self.__speed_download
	def get_speed_upload(self):
		return self.__speed_upload

	def update_speed_download(self):
		pass
	def update_speed_upload(self):
		pass

	def update_spped_statistics(self):
		pass

	def add_tracker(self, tracker):
		try:
			self.__trackers.append(tracker)
			return True
		except:
			return False
	def rem_tracker(self, tracker):
		try:
			self.__trackers.remove(tracker)
			return True
		except:
			return False