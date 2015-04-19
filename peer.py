import  address
import tracker
import leecher, seed

class Peer(leecher.Leecher, seed.Seed):
	"""docstring for Peer"""
	__address = None
	__speed_download = None
	__speed_upload = None
	__trackers = None

	def __init__(self, address = None, spped_download = 0.0, spped_upload = 0.0, trackers = []):
		self.__address = address
		self.__speed_download = spped_download
		self.__speed_upload = spped_upload
		self.__trackers = trackers
	def __eq__(self, peer):
		return self.__address == peer.__address

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




		