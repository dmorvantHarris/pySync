import socket
import sys
import signal
import time

killCmd = False

def sig_handle(signum, frame):
	print "Closing..."
	killCmd = True	
	

serverIp = "127.0.0.1"
serverPort = 50505
bufferSize = 1024
isServer = False
passwd = "1234"
remoteFileName = "a.out"
localFileName = "test2.txt"
killCmd = False
signal.signal(signal.SIGINT, sig_handle)

if len(sys.argv) > 1:
	if sys.argv[1].lower() in "server":
		isServer = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server
if isServer:
	sock.bind(("", serverPort))
	sock.listen(1)
	sock.settimeout(5.0)
	while (not killCmd):
		try:
			conn, addr = sock.accept()
			toExit = False
			print "Connection from: ", addr
			data = conn.recv(bufferSize)
			if passwd in data:
				print "Verification complete."
				f = open(remoteFileName, 'rb')
				data = f.read(bufferSize)
				print "Sending data"
				conn.send(data)
				print "Sent Data"
				while data != "":
					data = f.read(bufferSize)
					conn.send(data)
				time.sleep(.1)
				conn.send("EOF")
				print "All data sent"
		except socket.timeout:
			print "Server Timeout"
			
else:
	sock.settimeout(5.0)
	sock.connect((serverIp, serverPort))
	sock.send(passwd)
	notExit = True
	f = open(localFileName, "wb")
	data2 = ""
	data = ""
	while notExit:
		try:
			print "Writing..."
			print data2
			print data
			f.write(data2)
			data2 = data
			data = sock.recv(bufferSize)
			print data
		except socket.timeout:
			if data == "EOF":
				print "Connection Closing"
			else:
				print "Timeout has occured"
			notExit = False
			

sock.close()


