#!/usr/bin/python3

import sys
import socket
import struct
import re
import random
import string
import math
import base64

PORT = 16742

CHECKER_STATUS_OK = 101
CHECKER_STATUS_CORRUPT = 102
CHECKER_STATUS_MUMBLE = 103
CHECKER_STATUS_DOWN = 104
CHECKER_STATUS_ERROR = 110

MAP_DIRECTORY = "map/"

TOTAL_WIDTH = 3000
TOTAL_HEIGHT = 3000

REGION_WIDTH = 300
REGION_HEIGHT = 300

MAX_ALLOWED_WIDTH = 15

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "<%d, %d>" % (self.x, self.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __hash__(self):
		return self.x * 3000 + self.y;


def load_points(region_x, region_y):
	filename = MAP_DIRECTORY + '%04X%04X.map' % (region_x, region_y)

	with open(filename, 'rb') as f:
		data = f.read()
		for i in range(0, len(data), 4):
			chunk = data[i:i+4]
			x, y = struct.unpack('hh', chunk)
			yield Point(x, y)

def jp_point_substract(a, b):
	return Point(a.x - b.x, a.y - b.y)

def jp_cross_product(a, b):
	return a.x * b.y - a.y * b.x

def jp_dot_product(a, b):
	return a.x * b.x + a.y * b.y

def jp_length_squared(a):
	return jp_dot_product(a, a)

def is_eligible(source, destination, p):
	a = jp_point_substract(destination, source)
	b = jp_point_substract(p, source)
	c = jp_point_substract(destination, p)
	a_b_cp = jp_cross_product(a, b)
	a_b_dp = jp_dot_product(a, b)
	a_c_dp = jp_dot_product(a, c)

	return a_b_cp * a_b_cp <= MAX_ALLOWED_WIDTH * MAX_ALLOWED_WIDTH * jp_length_squared(a) and a_b_dp >= 0 and a_c_dp >= 0


def get_path(source, destination):
	min_x = min(source.x, destination.x) // REGION_WIDTH
	max_x = max(source.x, destination.x) // REGION_WIDTH
	min_y = min(source.y, destination.y) // REGION_HEIGHT
	max_y = max(source.y, destination.y) // REGION_HEIGHT

	for i in range(min_x, max_x + 1):
		for j in range(min_y, max_y + 1):
			for point in load_points(i, j):
				if is_eligible(source, destination, point):
					yield point

def communicate(host, data):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((host, PORT))
		sock.sendall(data)
		length = sock.recv(2)
		if len(length) < 2:
			sys.stderr.write('Service failed to send data lenght\n')
			sys.exit(CHECKER_STATUS_MUMBLE)
		length = struct.unpack('h', length)[0]
		return sock.recv(length)
	except socket.error:
		sys.exit(CHECKER_STATUS_DOWN)
	except Exception:
		sys.exit(CHECKER_STATUS_MUMBLE)
	finally:
		sock.close()

def chunk_to_point(chunk):
	try:
		x, y = struct.unpack('hh', chunk)
		return Point(x, y)
	except Exception:
		return None

def jetpack_get(host, source, destination, flag_id, flag):
	path_data = communicate(host, b'\x00' + flag_id + flag.encode())
	path = []
	for i in range(0, len(path_data), 4):
		path.append(chunk_to_point(path_data[i:i + 4]))
	control_path = list(get_path(source, destination))
	if set(path) != set(control_path):
		sys.stderr.write('Wrong path. Expected "%s", but was "%s"\n' % 
			(", ".join([ '<%d, %d>' % (p.x, p.y) for p in control_path ]),
				", ".join([ '<%d, %d>' % (None if p is None else p.x, None if p is None else p.y) for p in path ])))
		sys.exit(CHECKER_STATUS_MUMBLE)


def jetpack_list(host, flag_id):
	flags = communicate(host, b'\x01' + flag_id)
	return [ ba.decode('utf-8') for ba in re.findall(b'.{32}', flags) ]

def clamp(value, min_value, max_value):
	return max(min(value, max_value), min_value)

def check(host):
	flag = ''.join([ random.choice(string.ascii_letters + string.digits) for e in range(31) ]) + '='
	flag_id = put(host, flag)
	if not get(host, flag_id, flag):
		sys.exit(CHECKER_STATUS_MUMBLE)

def generate_heading():
	source = Point(random.randint(0, TOTAL_WIDTH - 1), random.randint(0, TOTAL_HEIGHT - 1))
	destination = Point(
		clamp(source.x + random.randint(-50, 50), 0, TOTAL_WIDTH - 1),
		clamp(source.y + random.randint(-50, 50), 0, TOTAL_HEIGHT - 1))
	return source, destination

def put(host, flag):
	source, destination = generate_heading()
	while len(list(get_path(source, destination))) == 0:
		source, destination = generate_heading()
	flag_id = struct.pack('hhhh', source.x, source.y, destination.x, destination.y)
	jetpack_get(host, source, destination, flag_id, flag)
	return flag_id

def get(host, flag_id, flag):
	flags = jetpack_list(host, flag_id)
	return flag in flags

mode = sys.argv[1]

if mode == 'check':
	check(sys.argv[2])
if mode == 'put':
	flag_id = put(sys.argv[2], sys.argv[4])
	print(base64.b64encode(flag_id).decode('utf-8'))
if mode == 'get':
	if not get(sys.argv[2], base64.b64decode(sys.argv[3]), sys.argv[4]):
		sys.exit(CHECKER_STATUS_CORRUPT)

sys.exit(CHECKER_STATUS_OK)