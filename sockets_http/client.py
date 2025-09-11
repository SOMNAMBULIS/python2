import socket


HOST = ('127.0.0.1', 7777)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


sock.connect(HOST)

try:
	while True:
		s = str(input('Enter data: ') or 'stop')
		sock.sendall(s.encode())
		if s == 'stop':
			break
except Exception as ex:
	print(ex)
finally:
	sock.close()

