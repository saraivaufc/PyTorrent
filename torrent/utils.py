import json, hashlib

def dict_to_binary(the_dict):
	str = json.dumps(the_dict)
	binary = ' '.join(format(ord(letter), 'b') for letter in str)
	return binary


def binary_to_dict(the_binary):
	jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
	d = json.loads(jsn)  
	return d

def to_binary(string):
	return ' '.join(format(ord(x), 'b') for x in string)

def hash_for_file(path, block_size=256*128, hr=False):
    md5 = hashlib.md5()
    with open(path,'rb') as f: 
        for chunk in iter(lambda: f.read(block_size), b''): 
             md5.update(chunk)
    if hr:
        return md5.hexdigest()
    return md5.hexdigest()

def hash_for_string(string):
	return hashlib.md5(string).hexdigest()
