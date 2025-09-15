import socket

def send_comm(sock, comm):
	sock.sendall(comm.encode())
	print(sock.recv(1024).decode())
	
def reg(sock):
	login, password = [input(f'Enter {i}:') for i in ['login','password']]
	send_comm(sock, f'command:reg; login:{login}; password:{password}')

def log(sock):
	login, password = [input(f'Enter {i}:') for i in ['login','password']]
	send_comm(sock, f'command:singin; login:{login}; password:{password}')

def main():
	try:
		HOST = ('127.0.0.1',7777)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect(HOST)
			while True:
				match input('1. Regestration\n2. Sing in\n0. Exit\n'):
					case '1':
						reg(sock)
					case '2':
						log(sock)
					case _:
						print('Bye')
						send_comm(sock,'command:exit; login:0; password:0')
						#send_comm(sock,' login:0; password:0')
						break
		
	except Exception as ex:
		print(f'Fail client: {ex}')

		
if __name__ == '__main__':
	main()
