import socket


HOST = ('127.0.0.1', 7777)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()

print("--start--")
conn, addr = sock.accept()
try:
	while True:		
		data = conn.recv(1024).decode()
		print(data)    
		if data == 'stop':
		        break
	
except Exception as ex:
	print(ex)
finally:
	conn.close()
