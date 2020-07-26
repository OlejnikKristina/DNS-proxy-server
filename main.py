#192.168.1.1
import socket
import codecs

MAX_DATAGRAM_LEN = 512
DEAFAUL_PORT = 53
UDPHEADER_SIZE = 8
DATAGRAM_SIZE = 41

def getDomainName(datagram):
	print(type(datagram), " len: ", len(datagram))

	domainNameLen = len(datagram) - DATAGRAM_SIZE
	domainNameBites = datagram[13:13 + domainNameLen]
	domainName = []

	for c in domainNameBites:
		if c == 3:
			domainName.append(46)
		else:
			domainName.append(c)

	print("Domain Name [", domainName, "] ")

def acceptData():
	socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	socketUDP.bind(('127.0.0.1', DEAFAUL_PORT))
	datagram, address = socketUDP.recvfrom(MAX_DATAGRAM_LEN)
	print("Conected with: ", address)
	print("Datagram: ", datagram)
	socketUDP.sendto(datagram, address)
	getDomainName(datagram)
	socketUDP.close()

def main():
	print("Hello world!")
	acceptData()

main()
