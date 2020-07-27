#!/usr/bin/env python3

import socket
import yaml
from dnslib import DNSRecord, RR, QTYPE, A, RCODE, TXT, DNSHeader

from settings import Settings

DEAFAUL_PORT = 53
DATAGRAM_SIZE = 41

def create_refuse_respond(domain_name, conf):
	unpacked_datagram = DNSRecord.parse(conf.datagram)
	response = unpacked_datagram.reply()
	response.header.rcode = RCODE.REFUSED
	if conf.refuse_action == "NXDOMAIN":
		response.header.rcode = RCODE.NXDOMAIN
		response.add_answer(RR(domain_name, QTYPE.A, rdata=A("0.0.0.0")))
	elif  conf.refuse_action == "Not_resolved":
		response.add_answer(RR(domain_name, QTYPE.TXT, rdata=TXT("Not resolved"))),
	else:
		response.add_answer(RR(domain_name, QTYPE.A, rdata=A("0.0.0.0")))
	return DNSRecord.pack(response)

def send_dns_query(conf):
	sending_address = (conf.superior_dns_server, DEAFAUL_PORT)
	UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	UDPsocket.sendto(conf.datagram, sending_address)
	dns_respond, _ = UDPsocket.recvfrom(512)
	UDPsocket.close()
	return dns_respond

def is_domain_blacked(domain_name, conf):
	if domain_name in conf.blacklist:
		return True
	return False

def get_domain_name(datagram):
	domain_name_len = len(datagram) - DATAGRAM_SIZE
	domain_nameBytes = datagram[13:13 + domain_name_len]
	domain_name = []
	for c in domain_nameBytes:
		if c == 3:
			domain_name.append('.')
		else:
			domain_name.append(chr(c))
	domain_name = ''.join(domain_name)
	return domain_name

def main():
	UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	UDPsocket.bind(('127.0.0.1', DEAFAUL_PORT))
	datagram, address = UDPsocket.recvfrom(512)
	# Init struct, read config file
	conf = Settings(datagram, address, UDPsocket)
	domain_name = get_domain_name(datagram)
	if not is_domain_blacked(domain_name, conf):
		ansswer = send_dns_query(conf)
	else:
		ansswer = create_refuse_respond(domain_name, conf)
	UDPsocket.sendto(ansswer, address)
	UDPsocket.close()

main()
