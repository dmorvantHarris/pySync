import socket
import sys

serverIp = "127.0.0.1"
serverPort = 50505
bufferSize = 1024
isServer = False
passwd = "1234"
remoteFileName = "test.txt"
localFileName


if sys.argv[1].lower() in "server":
	isServer = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server
if isServer:
	sock.bind(("", serverPort))
	sock.listen(1)
	sock.settimeout(5.0)
	while (1):
		conn, addr = s.accept()
		toExit = False
		print "Connection from: ", addr
		data = conn.recv(bufferSize)
		if passwd in data:
			print "Verification complete."
			f = open(remoteFileName, 'rb')
			data = f.read(bufferSize)
			conn.send(data)
			while data != "":
				data = f.read(bufferSize)
				conn.send(data)
			conn.send("EOF")
			
else:
	sock.settimeout(5.0)
	sock.connect((serverIp, serverPort))
	sock.send(passwd)
	notExit = True
	f = open(localFileName, "wb")
	while notExit:
		try:
			f.write(data2)
			data2 = data
			data = sock.recv(bufferSize)
		except socket.timeout:
			if data == "EOF":
				print "Connection Closing"
			else:
				print "Timeout has occured"
			notExit = False
			



