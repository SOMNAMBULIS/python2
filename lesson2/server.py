import socket
import re
import datetime


def send_comm(conn, comm):
	conn.sendall(comm.encode())

def reg(conn, login, password):
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if not check(login):
		send_comm(conn, 'Данный пользователь уже существует')
	elif not check_valid(login, password):
		send_comm(conn, '{time} - ошибка регистрации {login} - неверный пароль/логин')
	else:
		with open('log_pass.txt', 'a') as l:
			l.write(f'{login}:{password}\n')
		send_comm(conn, f'{time} -  пользователь {login} зарегистрирован')	
	
def log(conn, login, password):
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	with open('log_pass.txt', 'r') as l:
		for i in l.readlines():
			if login == i.split(':')[0] and password == i.split(':')[1][:-1]:
				send_comm(conn, f'{time} - пользователь {login} произведен вход')
				return None
		send_comm(conn, f'{time} - ошибка входа {login} - неверный пароль/логин')
			
				
def check_valid(login, password):
	return True if re.search(r'^[a-zA-Z0-9]{6,}$', login) and re.search(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9]{8,}$', password) else False

def check(login):
	with open('log_pass.txt', 'r') as l:
		return not login in [i.split(':')[0] for i in l.readlines()]
			

def main():
	try:
		HOST = ('127.0.0.1',7778)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.bind(HOST)
			sock.listen()
			print('Listen')
			conn, addr = sock.accept()
			while True:
				data = conn.recv(1024).decode()
				print(data)
				comm = data.split('; ')[0].split(':')[1]
				login = data.split('; ')[1].split(':')[1]
				password = data.split('; ')[2].split(':')[1]
				match comm:
					case 'reg':
						reg(conn, login, password)
					case 'singin':
						log(conn, login, password)
					case _:
						conn.close()
						print(111, conn)
						break


	except Exception as ex:
		print(f'Fail server: {ex}')		
	
		
if __name__ == '__main__':
	main()
