#!/usr/bin/env python3

import socket
import yaml

MAX_DATAGRAM_LEN = 512
DEAFAUL_PORT = 53
DATAGRAM_SIZE = 41

def isDomainInBlackList(domainName, blacklist, banMsg):
	if domainName in blacklist:
		print("\"", domainName, "\"", banMsg)
		return True
	return False

def readSettings(domainName):
	with open('DNSProxyServer.conf') as f:
		config = yaml.safe_load(f)

	blacklist = config["blacklist"]
	print("blacklist: ", blacklist)

	superiorDNSServer = config["superiorDNSServer"]
	print("superiorDNSServer: ", superiorDNSServer)

	banMsg = config["banMsg"]
	print("banMsg: ", banMsg)

	isInBlackList(domainName, blacklist, banMsg)

def getDomainName(datagram):
	print(type(datagram), " len: ", len(datagram))

	domainNameLen = len(datagram) - DATAGRAM_SIZE
	domainNameBytes = datagram[13:13 + domainNameLen]
	domainName = []

	for c in domainNameBytes:
		if c == 3:
			domainName.append('.')
		else:
			domainName.append(chr(c))
	domainName = ''.join(domainName)
	return domainName

def acceptData():
	socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	socketUDP.bind(('127.0.0.1', DEAFAUL_PORT))
	datagram, address = socketUDP.recvfrom(MAX_DATAGRAM_LEN)
	# print("Conected with: ", address)
	# print("Datagram: ", datagram)
	socketUDP.sendto(datagram, address)
	domainName = getDomainName(datagram)
	readSettings(domainName)
	socketUDP.close()

def main():
	acceptData()

main()
