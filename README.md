# DNS-proxy-server
Simple DNS proxy server with support of domain name's blacklist.
The program checks if requested domain name located in the blacklist specified by configuration file `DNSProxyServer.conf`.
If it's so, the refuse DNS response will be generated according to parameters set in configuration file.
Otherwise, it will send DNS request to superior DNS server, which also specified in configuration file.

## Usage
`git clone https://github.com/OlejnikKristina/DNS-proxy-server.git`<br/>
`cd DNS-proxy-server`<br/>
`sudo python3 DNSProxyServer.py`<br/>
In other terminal type: `dig [Any Doname Name] @localhost` <br/>
Example: `dig youtube.com @localhost`

## Requirements
You need to have instaled: <br/>
  Python 3.6.9 <br/>
  pyyaml <br/>
  dnslib<br/>
  
### Environment
WSL Ubuntu

### Bugs
Please open an 'issues' if you find any bugs.
