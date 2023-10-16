#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @m8sec
# License: BSD 3-Clause License
#
# Copyright (c) 2023, m8sec
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import re
import logging
import ipaddress
from os import path
import dns.resolver
from random import shuffle
from sys import exit, stdin
from re import compile, match
from ipparser.nmap import nmap_xml_parser

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

class IPParser:
    '''
    primary class used to parse user input and return array
    of sorted ip addresses or target name for iteration.
    '''

    regex = {
        'cidr': compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$"),
        'range': compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}$"),
        'dns': compile("^.+\.[a-z|A-Z]{2,}$")
    }

    def __init__(self, open_ports=False, exit_on_err=False, resolve=False, ns=[]):
        self.exit_on_err = exit_on_err
        self.open_ports = open_ports
        self.resolve = resolve
        self.hosts = []
        self.ns = ns

    def parse(self, targets):
        for t in targets:
            self.controller(t)
        return self.hosts

    def controller(self, target):
        try:
            # Take in host input & send to associated method
            if target.lower().endswith('.txt'):
                LOG.debug('IPParser: Processing Txt input')
                self.file_parser(target)

            elif target.lower().endswith('.xml'):
                LOG.debug('IPParser: Processing xml input')
                if path.exists(target):
                    return nmap_xml_parser(target, self.open_ports)
                else:
                    raise Exception('IPParser ERR: Input file not found.')

            elif match(self.regex['range'], target):
                LOG.debug('IPParser: Processing range input')
                self.range_parser(target)

            elif ',' in target:
                LOG.debug('IPParser: Processing comma delimited input')
                self.multi_parser(target)

            elif match(self.regex['dns'], target) and "," not in target:
                LOG.debug('IPParser: Processing DNS host input')
                if self.resolve:
                    ip = resolve_dns(target, ns=self.ns)
                    self.hosts.append(ip) if ip not in self.hosts else False
                else:
                    self.hosts.append(target) if target not in self.hosts else False

            elif match(self.regex['cidr'], target):
                LOG.debug('IPParser: Processing CIDR input')
                for ip in ipaddress.ip_network(target, strict=False):
                    self.hosts.append(str(ip))
            else:
                LOG.debug('IPParser: Processing single IP or URL input')
                self.hosts.append(target) if target not in self.hosts else False

        except Exception as e:
            LOG.debug(f'IPParser ERR: {e}')
            exit(1) if self.exit_on_err else False
        return self.hosts

    def ip_parser(self, ip):
        try:
            # Return True on valid IPv4/IPv6 address (not in use)
            return ipaddress.ip_address(str(ip))
        except:
            return False

    def file_parser(self, filename):
        if path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    line.strip()
                    self.controller(line.strip())
        else:
            raise Exception('IPParser ERR: Input file not found.')

    def multi_parser(self, target):
        for t in target.strip().split(','):
            self.controller(t)

    def range_parser(self, target):
        a = target.split("-")
        b = a[0].split(".")
        for x in range(int(b[3]), int(a[1]) + 1):
            tmp = b[0] + "." + b[1] + "." + b[2] + "." + str(x)
            self.hosts.append(tmp) if target not in self.hosts else False


def iphandler(t_input, open_ports=False, exit_on_error=True, randomize=False, resolve=False, ns=[]):
    # Parse single target input as string and return array
    try:
        tmp = IPParser(open_ports, exit_on_error, resolve, ns)
        parser = tmp.parse if isinstance(t_input, list) else tmp.controller
        hosts = parser(t_input)
        return shuffle(hosts) if randomize else hosts
    except Exception as e:
        raise Exception(f'IPParser Err: {e}')


def ipparser(t_input=False, open_ports=False, exit_on_error=True, randomize=False, resolve=False, ns=[], debug=False):
    # Allows CLI based tooling to support multiple input types
    # debug=False - placeholder for backwards compatibility (will be removed in next version)
    data = []

    # Accept stdin
    if not stdin.isatty():
        for x in stdin:
            data = data + iphandler(str(x).strip(), open_ports, exit_on_error, randomize, resolve, ns) if x else data

    # Accept array
    elif isinstance(t_input, list):
        for x in t_input:
            if stdin.isatty():
                data = data + iphandler(str(x).strip(), open_ports, exit_on_error, randomize, resolve, ns) if x else data

    # Accept String
    else:
        data = data + iphandler(str(t_input).strip(), open_ports, exit_on_error, randomize, resolve, ns) if t_input else data
    return data


def resolve_dns(host, qtype="A", ns=[], tcp=False, timeout=3):
    result = host
    try:
        res = dns.resolver.Resolver()
        res.lifetime = timeout
        if ns:
            res.nameservers = [ns] if type(ns) == str else ns
        dns.resolver.override_system_resolver(res)
        dns_query = res.resolve(host, qtype, tcp=tcp)
        # Return first resolved IP
        result = str(dns_query[0])
    except Exception as e:
        LOG.debug(f'IPParser ERR: Failed to resolve {host} - {e}')
    return result


def host_parser(host, default_proto=['http', 'https'], default_port=False, default_pages=['/']):
    # Normalize various host inputs and return dict of parsed values
    tmp = {'proto': default_proto, 'host': False, 'port': default_port, 'page': default_pages}

    regex = [
        # http://example.com:8080/page
        r'(.*)://(.*):([0-9]+)(/.*)',
        # http://example.com/page/index.html
        r'(.*)://([^/]+)()(.*.)',
        # http://example.com/internal/
        r'(.*)://([^/]+)()(.*/)',
        # http://example.com:8080
        r'(.*)://(.*):([0-9]+)()',
        # http://example.com
        r'(.*)://(.*)()()',
        # example.com:8080/page
        r'()(.*):([0-9]+)(/.*)',
        # example.com:8080
        r'()(.*):([0-9]+)()',
        # example.com
        r'()(.+\.[a-z|A-Z]{2,})()()',
        # 192.168.1.1
        r'()(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})()()',
    ]

    for pattern in regex:
        r = re.search(pattern, host)
        if r is not None:
            tmp['proto'] = [r.group(1).lower()] if r.group(1) else tmp['proto']
            tmp['host'] = r.group(2) if r.group(2) and ':' not in r.group(2) else tmp['host']
            tmp['port'] = r.group(3) if r.group(3) else tmp['port']
            tmp['page'] = [r.group(4)] if r.group(4) else tmp['page']
            return tmp
    return tmp
