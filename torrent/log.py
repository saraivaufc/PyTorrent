import json, os.path

class Log():
    """docstring for Log"""
    __path = None
    __hash = None
    __last_modification = None
    __size = 0
    __qtd_parts = 0
    __qtd_parts_remainder = None
    def __init__(self, path, hash_file=None, last_modification = None, size = 0, qtd_parts = 0):
        self.__path = path
        self.__hash = hash_file
        self.__last_modification = last_modification
        self.__size = size
        self.__qtd_parts = qtd_parts
        self.__qtd_parts_remainder = qtd_parts
    def get_path(self):
        return self.__path
    def get_hash(self):
        return self.__hash
    def get_last_modificatiion(self):
        return self.__last_modification
    def get_size(self):
        self.__size
    def get_qtd_parts(self):
        return self.__qtd_parts
    
    def set_path(self, path):
        self.load()
        self.__path = path
        self.save()
    def set_hash(self, hash_file):
        self.load()
        self.__hash = hash_file
        self.save()
    def set_last_modification(self, last_modification):
        self.load()
        self.__last_modification = last_modification
        self.save()
    def set_size(self, size):
        self.load()
        self.__size = size
        self.save()
    def set_qtd_parts(self, qtd_parts):
        self.load()
        self.__qtd_parts = qtd_parts
        self.save()
    def decrement_parts_remainder(self):
        self.load()
        self.__qtd_parts_remainder = self.__qtd_parts_remainder - 1
        if self.__qtd_parts_remainder < 0:
            self.__qtd_parts_remainder = 0
        self.save()
        
    def increment_parts_remainder(self):
        self.load()
        self.__qtd_parts_remainder = self.__qtd_parts_remainder + 1
        self.save()
        
    def load(self):
        try:
            f = open(self.__path+ ".log", "r").read()
        except:
            print ".log nao encontrado"
            return
        try:
            msn = json.loads(f)
            self.__path = msn["path"]
            self.__hash = msn["hash"]
            self.__last_modification = msn["lash_modification"]
            self.__size = msn["size"]
            self.__qtd_parts = msn["qtd_parts"]
            self.__qtd_parts_remainder = msn["qtd_parts_remainder"]
            return True
        except:
            return False
        
    def save(self):
        f = open(self.__path + ".log", "w")
        msn = json.dumps({"path": self.__path, 
                          "hash": self.__hash,
                          "lash_modification": str(self.__last_modification),
                          "size": self.__size,
                          "qtd_parts": self.__qtd_parts,
                          "qtd_parts_remainder": self.__qtd_parts_remainder })
        f.write(msn)
        f.close()
    def exists(self):
        return os.path.exists(self.__path)
    def is_complete(self):
        self.load()
        return self.__qtd_parts_remainder == 0 and self.__qtd_parts > 0