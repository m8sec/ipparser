#!/usr/bin/env python3
# Description: Test ipparser module

import sys
import logging
sys.path.append('..')
from os import remove
from ipparser import ipparser


def setup_debug_logger():
    debug_output_string = "DEBUG %(message)s"
    formatter = logging.Formatter(debug_output_string)
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.propagate = False
    root_logger.addHandler(streamHandler)
    root_logger.setLevel(logging.DEBUG)
    return root_logger


if __name__ == '__main__':
    setup_debug_logger()

    print("[ * ] m8sec.dev, resolve=False, exit_on_error=True")
    tmp = ipparser('m8sec.dev', resolve=False)
    print("[<--] {}\n".format(tmp))

    print("[ * ] https://m8sec.dev, resolve=False, exit_on_error=True")
    tmp = ipparser('https://m8sec.dev', resolve=False)
    print("[<--] {}\n".format(tmp))
    
    print("[ * ] https://m8sec.dev:8080, resolve=False, exit_on_error=True")
    tmp = ipparser('https://m8sec.dev:8080', resolve=False)
    print("[<--] {}\n".format(tmp))

    print("[ * ] https://m8sec.dev:8080/default.aspx, resolve=False, exit_on_error=True")
    tmp = ipparser('https://m8sec.dev:8080/default.aspx', resolve=False)
    print("[<--] {}\n".format(tmp))

    print("[ * ] m8sec.dev, resolve=True, exit_on_error=True")
    tmp = ipparser('m8sec.dev', resolve=True)
    print("[<--] {}\n".format(tmp))

    print("[ * ] m8sec.demo.local, resolve=False, exit_on_error=True")
    tmp = ipparser('m8sec.demo.local', resolve=False)
    print("[<--] {}\n".format(tmp))

    print("[ * ] 192.168.1.0/24, resolve=False, exit_on_error=True")
    tmp = len(ipparser('192.168.1.0/24', resolve=False))
    print("[<--] count: {}\n".format(tmp))

    print("[ * ] 192.168.1.0/16, resolve=False, exit_on_error=True")
    tmp = len(ipparser('192.168.1.0/16', resolve=False))
    print("[<--] count: {}\n".format(tmp))

    print("[ * ] 10.0.0.1-5, resolve=False, exit_on_error=True")
    tmp = ipparser('10.0.0.1-5', resolve=False)
    print("[<--] {}\n".format(tmp))

    print("[ * ] 10.0.0.1,192.168.1.1, resolve=False, exit_on_error=True")
    tmp = ipparser('10.0.0.1,192.168.1.1', resolve=False)
    print("[<--] {}\n".format(tmp))

    print("[ * ] 10.0.0.1,google-public-dns-a.google.com, resolve=True, exit_on_error=True")
    tmp = ipparser('', resolve=True)
    print("[<--] {}\n".format(tmp))

    print("[ * ] 10.0.0.1,m8sec.dev, resolve=False, exit_on_error=True")
    tmp = ipparser('', resolve=False)
    print("[<--] {}\n".format(tmp))

    print("[ * ] 10.0.0.1. resolve=False, exit_on_error=True")
    tmp = ipparser('', resolve=False)
    print("[<--] {}\n".format(tmp))


    op = open('tmp.txt', 'w')
    op.write('127.0.0.1\n')
    op.write('google-public-dns-a.google.com\n')
    op.write('10.0.0.1,10.0.0.2\n')
    op.write('172.16.0.1-25\n')
    op.close()

    print("[ * ] tmp.txt, resolve=False, exit_on_error=True")
    tmp = ipparser('tmp.txt')
    print("[<--] {}\n".format(tmp))

    print("[ * ] tmp.txt, resolve=True, exit_on_error=True")
    tmp = ipparser('tmp.txt', resolve=True)
    print("[<--] {}\n".format(tmp))
    
    remove('tmp.txt')
