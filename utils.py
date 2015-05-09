import json
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
