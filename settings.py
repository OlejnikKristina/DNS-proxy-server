
import yaml

class Settings:
	def __init__(self, DNSdatagram, address, sock):
		with open('DNSProxyServer.conf') as f:
			config = yaml.safe_load(f)
		self.blacklist = config["blacklist"]
		self.superior_dns_server = config["superior_dns_server"]
		self.refuse_action = config["refuse_action"]
		self.datagram = DNSdatagram
		self.UDPsocket_addr = address
		self.UDPsocket = sock
