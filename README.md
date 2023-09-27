# IPParser

The IPParser Python library was created to simplify accepting IP addresses, DNS names, and target / host information in security or network based tooling.

User inputs are parsed to provide an iterable list for further action. If called with ```resolve=True```, ipparser will attempt to perform an "A" record lookup and return the first resolved address associated with the host.

#### Inputs:
IPParser currently accepts the following user inputs:
* Single IP (192.168.1.10)
* IP ranges (192.168.1.1-55)
* Multiple IP's (192.168.1.3,192.168.1.7,m8sec.dev)
* CIDR Ranges /8-/32 (192.168.1.0/24)
* URL's (https://m8sec.dev)
* IP:Port (192.168.1.1:8080)
* DNS Names (m8sec.dev)
* TXT files (Containing any of the items listed)
* Nmap XML Reports
* Read from STDIN

## Install
```bash
pip3 install ipparser
```
OR 
```bash
git clone https://github.com/m8sec/ipparser
cd ipparser
python3 setup.py install
```

## (Primary) Usage:
The IPParser function can be called with the following arguments (shown with their default values):
* ```open_ports=False``` - Return IP:Port notation for all open ports found (Nmap XML only)
* ```exit_on_error=True``` - Exit on error while parsing user input.
* ```resolve=False``` - Resolve any DNS names identified, to IPv4 addresses, and append to output.
* ```ns=[]``` - Define name servers for DNS lookups.

## Examples
#### Standard Usage
```python
>>> from ipparser import ipparser
>>> ipparser('192.168.1.3-5')
['192.168.1.3', '192.168.1.4', '192.168.1.5']

>>> ipparser('yahoo.com',resolve=True)
['74.6.143.26']


>>> ipparser('192.168.1.1,yahoo.com')
['192.168.1.1', 'yahoo.com']
```

#### Argparse Integration - Required Positional Argument:
```python
from ipparser import ipparser
from argparse import ArgumentParser

args = ArgumentParser(description='ipparser integration with argparse')
args.add_argument(dest='positional_host', nargs='+', type=lambda x: ipparser(x, resolve=False), help='Host Input')
args = args.parse_args()
```
```
Namespace(positional_host=[['192.168.1.1']])
```
