import  address
#import tracker
import socket
import pickle
from threading import Thread
import file

buffer = 65507

# max 65536 Bytes


class Peer():
	"""docstring for Peer"""
	__address = None
	__speed_download = None
	__speed_upload = None
	__trackers = None
	__files_upload = None
	__files_download = None
	__socket_peer_download = None
	__socket_peer_upload = None
	__parts_requested = None

	def __init__(self, address = None, trackers = []):
		self.__address = address
		self.__speed_download = 0.0
		self.__speed_upload = 0.0
		self.__files_download = {}
		self.__files_upload = {}
		self.__trackers = trackers
		self.__parts_requested = {}
	def __eq__(self, peer):
		return self.__address.get_ip() == peer.__address.get_ip()

	def run(self):
		self.__socket_peer_download = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__socket_peer_upload = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		

	# Path references .pytorrent
	def download(self, path):
		th=Thread( target=self.download_thread,
					args = ( path, ) )
		th.start()
		
	def download_thread(self, path):
		f = file.File(path)
		hash_file = f.get_hash()
		self.__files_download[hash_file] = f
		#para cada uma das partes
		for i in f.get_parts():
			hash_part = i.get_hash()
			message = pickle.dumps({"type":3, "file": hash_file, "part": hash_part })

			#para cada um dos trackers
			for k in self.__trackers:
				self.__socket_peer_download.sendto(message, (k.get_address().get_ip(),k.get_address().get_port()))
				print "Peer download- eu " + str(self.__socket_peer_download.getsockname()) + " pedir ao tracker " + str(k.get_address()) + "a lista dos peer dese arquivo"
			while 1:
				#response in 30
				message, tracker_address = self.__socket_peer_download.recvfrom(buffer)
				print "Peer download- eu " + str(self.__socket_peer_download.getsockname()) + " recebi do tracker" + str(tracker_address) + "a lista dos peers"
				try:
					message = pickle.loads(message)
					th=Thread( target=self.download_part_thread,
								args = ( hash_file,hash_part, message ) )
					th.start()
				except:
					print "Falha ao carregar a resposta"
				#break
	def download_part_thread(self, hash_file, hash_part, message):
		for i in message["address_peers"]:
			msn = pickle.dumps({"type": 1,"file": hash_file, "part" : hash_part})
			socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			socket_cliente.sendto(msn, i )
			print "Peer download: "+ str(socket_cliente.getsockname()) +"  requisitei ao peer " + str(i) + "um data de uma parte"
			th=Thread( target=self.download_part_peer,
						args = ( hash_file,hash_part, socket_cliente) )
			th.start()

	def download_part_peer(self, hash_file, hash_part, socket_cliente):
		while 1:
			message, peer_address = socket_cliente.recvfrom(buffer)
			print "Pee download, "+ str(socket_cliente.getsockname()) +" recebi do peer " + str(peer_address) + "um arquivo"
			print "Receebi=" + str(len(message))
			try:
				message = pickle.loads(message)
			except:
				print "Erro ao Converter"
				return
			hash_file = message["file"]
			data = message["data"]
			f = file.File("saida/saida.mp3")
			f.data_to_part(data)
			# if f.is_complete():
			# 	f.merge()
			# 	break





	def upload(self, path):
		th=Thread( target=self.upload_thread,
					args = ( path, ) )
		th.start()
	def upload_thread(self, path):
		f = file.File(path)
		self.__files_upload[f.get_hash()] = f
		f.divider_parts()
		for i in f.get_parts():
			message = pickle.dumps({"type": 2, "file": f.get_hash(), "part": i.get_hash() })
			for k in self.__trackers:
				self.__socket_peer_upload.sendto(message, (k.get_address().get_ip(),k.get_address().get_port()))
				print "Peer upload : Eu "+  str(self.__address) +"  mandei um arquivo pro tracker " + str(k.get_address())
		while 1:
			message, peer_address = self.__socket_peer_upload.recvfrom(buffer)
			message = pickle.loads(message)
			if int(message["type"]) == 1:
				print "Peer upload : Eu " + str(self.__address) + "recebi do Peer " + str(peer_address) + "um pedido de arquivo" 
				th=Thread( target=self.upload_part_thread,
						args = ( message["file"], message["part"], peer_address))
				th.start()
			else:
				print "Peer upload: "+ str(self.__address) +", O Tracker " + str(peer_address) + "confirmou o recebimento do meu upload"

	def upload_part_thread(self,hash_file, hash_part, address):
		response = ""
		try:
			f = self.__files_upload[hash_file]
			data = f.part_to_data_in_parts(hash_part)
			response = pickle.dumps({"type": 10, "file": hash_file, "part": hash_part, "data": data })
		except:
			response = "404"
		print "Tamanho para enviar = " + str(response)
		self.__socket_peer_upload.sendto(response, address)
		print "Peer upload: Eu " + str(self.__address) + "respondi com a parte ao peer " + str(address)


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