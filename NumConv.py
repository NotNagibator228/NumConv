from sys import argv, exit
from dataclasses import dataclass
from os.path import exists
from math import log10

@dataclass
class db:
	char : str
	index : int

	def __init__(self, char : str, index : int):
		self.char = char
		self.index = index

class uncov_alphabet:
	def __init__(self, line : str):
		self.line = [ db(line[i], i) for i in range(len(line)) ]
		sorted(self.line, key=lambda x: x.char)

	def find(self, char : str):
		begin, end = 0, len(self.line)
		while begin <= end:
			index = (begin + end) // 2
			if char < self.line[index].char:
				end = index - 1
			elif char > self.line[index].char:
				begin = index + 1
			else: return self.line[index].index
		return -1

	def __len__(self):
		return len(self.line)

default_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph = []
index : int
length = 10
argb = [ False for _ in range(0, 5) ]
argo = (
	'version',
	'about',
	'help'
)

def error_args(line : str, exit_code : int):
	print ('Error', line)
	print (argo[2])
	exit(exit_code)

def line_args(index : int):
	max = index + 5 if len(argv) - index > 4 else len(argv)
	count = 0

	for element in argv[index:]:
		if element[0] == '-': break
		else: count = count + 1

	alph.append( (1, index, 0) )
	if count == 1 or count == 4: return 1
	elif count == 2 or count == 5:
		alph.append( (1, index + 1, 0) )
		return 2
	else: error_args('error args line count', 120)

def file_args(index : int):
	if not exists(argv[index]): error_args('file ' + argv[index] + ' no found', 130)
	if len(argv[index + 1]) > 2: error_args('many key file', 131)

	alph.append((2, index, 0))
	if len(argv[index + 1]) == 2: alph.append((2, index, 1))
	return 2

def load_file(path : str, key : str):
	with open(path, encoding='utf-8', mode = 'r') as file:
		for line in file:
			_line = line.rstrip()
			if _line[0] == key:
				if len(_line) > 3 and _line[1] == '\t': return _line[2:]
				else:
					print('Error format file\n')
					exit(132)
			print(_line)
	error_args('no found key ' + key + ' in file', 131)

def test_line(line : str):
	if len(line) < 2: error_args('alphabet < 2', 142)
	test_set = set(line)
	if len(test_set) != len(line): error_args('error alphabet', 140)
	if ',' in test_set: error_args(', in alphabet', 141)

def args_length(index : int):
	global length
	length = int(argv[index])
	return 1

def uncov_number0(line : str, alphabet : uncov_alphabet):
	buffer = 0
	for element in line:
		num = alphabet.find(element)
		if num == -1:
			print('error uncov number')
			exit(200)
		buffer = buffer * len(alphabet) + num
	return buffer

def uncov_number(line : str, alphabet : str):
	num0, num1, max = 0, 0, line.find(',')
	if max == -1: max = len(line)
	alphi = uncov_alphabet(alphabet)

	num0 = uncov_number0(line[:max], alphi)
	if max != len(line): num1 = uncov_number0(line[max + 1:], alphi)
	return num0, num1

def conv_number(num0, num1, notation, line : str, n2 : int):
	buffer = ''
	#хз почему сдесь глючит с len(line) приходится использовать n2
	while True:
		buffer = buffer + line[num0 % n2]
		num0 = num0 // n2
		if num0 == 0: break
	buffer = buffer[::-1]

	if num1 > 0:
		global length
		len = notation ** (int(log10(num1)) + 1)
		buffer = buffer + ','
		count = 0

		while num1 > 0 and count < length:
			num, num1 = divmod(num1 * n2, len)
			buffer = buffer + line[num]
			count = count + 1

	return buffer

def conventor(line0, line1, line):
	num0, num1 = uncov_number(line, line0)
	print(conv_number(num0, num1, len(line0), line1, len(line1)))

def main():
	if len(argv) == 1:
		print ('Error no argument')
		exit(100)

	i = 1
	while i < len(argv):
		if argv[i][0] == '-':
			if argv[i][1] == '-':
				match argv[i][2:]:
					case 'version': argb[0] = True
					case 'about': argb[1] = True
					case 'help': argb[2] = True
					case 'line': i = i + line_args(i + 1)
					case 'file': i = i + file_args(i + 1)
					case 'default': alph.append((0, 0, 0))
					case 'length': i = i + args_length(i + 1)
					case _: error_args('no argumnet: ' + argv[i][2:], 101)
			else:
				b = 0
				for element in argv[i][1:]:
					match element:
						case 'v': argb[0] = True
						case 'a': argb[1] = True
						case 'h': argb[2] = True
						case 'l': b = b + line_args(i + b + 1)
						case 'f': b = b + file_args(i + b + 1)
						case 'd': alph.append((0, 0, 0))
						case 'L': b = b + args_length(i + b + 1)
						case _: error_args('no key: ' + element, 102)
				i = i + b
		elif (len(argv) - 2) > 0:
			if argb[4]: error_args('conventor reactivated', 103)
			index = i; i += 2; argb[4] = True
		else: error_args('count conventor', 104)
		i = i + 1

	for i in range(0, 3):
		if argb[i]:
			print (argo[i])
			argb[3] = True

	if argb[3]: exit(0)
	if not argb[4]: error_args('no conventor', 105)
	if len(alph) > 2: error_args('to many args alphabet', 106)

	line = [ '', '' ]
	if len(alph) > 0:
		for i in range(0, len(alph)):
			match alph[i][0]:
				case 0: line[i] = default_alphabet
				case 1: line[i] = argv[alph[i][1]]
				case 2: line[i] = load_file(argv[alph[i][1]], argv[alph[i][1] + 1][alph[i][2]])
			test_line(line[i])
		if len(alph) == 1: line[1] = line[0]
	else: line[0], line[1] = default_alphabet, default_alphabet

	num = [ 0, 0]
	num[0], num[1] = int(argv[index]), int(argv[index + 2])
	for i in range(0, 2):
		if num[i] < 2 or num[i] > len(line[i]):
			error_args('num < 2 or > len alphabet', 150)

	conventor(line[0][:num[0]], line[1][:num[1]], argv[index + 1])

if __name__ == '__main__': main()
