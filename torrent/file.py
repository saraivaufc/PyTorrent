# -*- encoding=utf-8 -*-

import datetime
import hashlib
import json
import os.path

import part
import utils

chunk = 569344
#chunk = 50000


class File(object):
    """docstring for File"""
    __path = None
    __hash = None
    __parts = None
    __is_load = False
    __last_modification = None
    __size = 0
    __qtd_parts = 0

    def __init__(self, path=None):
        self.__path = path
        self.__parts = {}
        self.__hash = self.get_hash_disk()
        self.__last_modification = datetime.datetime.now()
        self.load()

    def __eq__(self, part):
        return self.__hash == part.__hash

    def set_path(self, part):
        self.__path = part

    def set_hash(self, new_hash):
        self.__hash = new_hash

    def get_path(self):
        return self.__path

    def get_hash(self):
        return self.__hash

    def get_parts(self):
        return self.__parts

    def get_hash_disk(self):
        if os.path.exists(self.__path):
            return utils.hash_for_file(self.__path)
        else:
            return None

    def get_parts_not_found(self):
        not_found = []
        for part in self.__parts.values():
            try:
                data = part.get_data()
                hash_part = utils.hash_for_string(data)
                if data == None or part.get_hash() != hash_part:
                    not_found.append(part)
            except Exception, e:
                print e
                not_found.append(part)
        return not_found

    def get_size(self):
        return self.__size

    def data_to_part(self, data):
        hash_data = utils.hash_for_string(data)
        part_file = part.Part(hash_data, str(self.__hash) + "/")
        try:
            os.mkdir(str(self.__hash) + "/")
        except:
            pass
        part_file.set_data(data)
        self.__parts[hash_data] = part_file

    def part_to_data_in_parts(self, hash_part, dead=False):
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
        # -- "A part veio das Parts"
        return data

    def part_to_data_in_file(self, hash_part, dead=False):
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
        return data_file

    def merge(self):
        # se o arquivo ja existir
        if self.exist():
            print "O Arquivo final ja foi criado por outro merge"
            return True

        print "Fazendo o merge das Partes"
        f = open(self.__path, "wb")
        parts = self.__parts.values()
        parts.sort()
        for part in parts:
            f.write(part.get_data())
        f.close()
        if self.checksum():
            print "Depois de fazer o merge das partes, verifiquei o checksum e deu tudo OK!!! :)"
            return True
        else:
            print "Depois de fazer o merge das partes, verifiquei o checksum e deu ERRROOOOO!!! :("
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
            dict_data = json.loads(open(self.__path + ".pytorrent").read())
            print ".pytorrent FOUND 1 "
        except:
            try:
                dict_data = json.loads(open(self.__path).read())
                print ".pytorrent FOUND 2"
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
        self.__size = dict_data['size']
        self.__qtd_parts = dict_data['qtd_parts']
        parts_str = json.loads(dict_data['parts'])
        self.__parts = {}
        parts = parts_str["parts"]
        for i in parts:
            self.__parts[i["hash"]] = part.Part(i["hash"], self.__hash + "/", i["index"])
        self.__qtd_parts = len(parts)

        return True

    def divider_parts(self):
        print "Iniciando Particionamento do arquivo:" + self.__path
        try:
            f = open(self.__path, "rb")
            self.__size = os.path.getsize(self.__path)
        except Exception, e:
            print e
            print "Arquivo Not Found"
            return False
        f.seek(0, 2)
        size_file = f.tell()
        f.seek(0)
        self.__parts = {}
        while f.tell() < size_file:
            buffer_size = f.read(chunk)
            hash_part = hashlib.md5(buffer_size).hexdigest()
            part_file = part.Part(hash_part, str(self.__hash) + "/", f.tell())
            part_file.set_data(buffer_size)
            self.__parts[hash_part] = part_file
        self.__qtd_parts = len(self.__parts.keys())
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
        dict_data = {'hash': self.__hash,
                     'path': self.__path,
                     'size': self.__size,
                     'qtd_parts': self.__qtd_parts,
                     'parts': str(json_parts)}
        json.dump(dict_data, open(self.__path + ".pytorrent", "wb"))

    def is_complete(self):
        if self.exist():
            return True
        print "\nVerificando se todas as partes ja foram baixadas"
        print "\nQuantidades de arquivos no diretorio:", len(os.listdir(self.__hash + "/"))
        print "\nQuantidades de partes:", self.__qtd_parts

        if len(os.listdir(self.__hash + "/")) == self.__qtd_parts:
            if len(self.get_parts_not_found()) == 0:
                print "Todas as Partes ja foram baixadas!!!!\n"
                return self.merge()
            else:
                return False
        else:
            print "Ainda restam partes para serem baixadas!!!!\n"
            return False

    def exist(self):
        print "Verificando se o arquivo final ja foi criado"
        try:
            if self.get_hash() == self.get_hash_disk():
                return True
        except:
            return False
