import socket
import sys
import signal
import time
import hashlib
import os.path

killCmd = False

def sig_handle(signum, frame):
	print "Closing..."
	killCmd = True	
def getMd5(fileName):
	with open(fileName, 'rb') as tf:
		m = hashlib.md5()
		while 1:
			md5Data = tf.read(8192)
			if not md5Data:
				break
			m.update(md5Data)
		return m.hexdigest()
	
	

serverIp = "127.0.0.1"
serverPort = 50505
bufferSize = 1024
isServer = False
passwd = "1234"
remoteFileName = "test.txt"
# list of files that can be requested
reqFileList = "req.txt"
localFileName = "test2.txt"
killCmd = False
signal.signal(signal.SIGINT, sig_handle)

if len(sys.argv) > 1:
	if sys.argv[1].lower() in "server":
		isServer = True


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server
if isServer:
	rFile = open(reqFileList, "r")
	reqList = []
	for line in rFile:
		print line
		reqList.append(line.rstrip())
	sock.bind(("", serverPort))
	sock.listen(1)
	sock.settimeout(5.0)
	while (not killCmd):
		try:
			conn, addr = sock.accept()
			toExit = False
			print "Connection from: ", addr
			data = conn.recv(bufferSize)
			splitData = data.split("|")
			if len(splitData) < 1:
				print "Invalid connection"
				conn.close()
				continue
			if passwd in splitData[0]:
				print "Verification complete."
				# get filename
				if len(splitData) > 1:
					print "Client Requesting file: " + splitData[1] 
					remoteFileName = ""
					for i in reqList:
						print i
						if splitData[1] == i:
							print "Requested file found"
							remoteFileName = i
							break
				if remoteFileName == "":
					print "Client requesting invalid file: " + splitData[1]
					conn.send("EOF")
					conn.close()
					continue
				# get md5
				if len(splitData) > 2:
					if (getMd5(remoteFileName) in splitData[2]):
						print "Client md5 match"
						conn.send("EOF")
						conn.close()
						continue
				f = open(remoteFileName, 'rb')
				data = f.read(bufferSize)
				print "Sending data"
				conn.send(data)
				print "Sent Data"
				while data != "":
					data = f.read(bufferSize)
					conn.send(data)
				time.sleep(.1)
				f.close()
				conn.send("EOF")
				conn.close()
				print "All data sent"
		except socket.timeout:
			print "Server Timeout"
			
else:
	sock.settimeout(5.0)
	sock.connect((serverIp, serverPort))
	if os.path.isfile(localFileName):
		sock.send(passwd + "|" + localFileName + "|" + str(getMd5(localFileName)))
	else:
		sock.send(passwd + "|" + localFileName)
	notExit = True
	f = open(localFileName, "wb")
	data2 = ""
	data = ""
	while notExit:
		try:
			print "Writing..."
			#print data2
			#print data
			f.write(data2)
			data2 = data
			data = sock.recv(bufferSize)
			#print data
			if not data or data == "EOF":
				sock.send("ack")
		except socket.timeout:
			if data == "EOF":
				print "Connection Closing"
			else:
				print "Timeout has occured"
			notExit = False
		except socket.error, e:
			print "Socket error " + str(e)
			notExit = False
	f.close()
			

sock.close()


