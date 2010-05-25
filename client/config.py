#!/usr/bin/python
# -*- coding: utf-8 -*-
#    This file is part of corvogame.
#
#    corvogame is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    corvogame is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with corvogame.  If not, see <http://www.gnu.org/licenses/>.

import ConfigParser
from optparse import OptionParser

configdefaults = {
    'loglevel': 'DEBUG',
    'server': '127.0.0.1',
    'port': '5000',
    'protocol': 'json',
    'username': 'anonymous',
    'password': '',
} # DEPRECATED
# OptionParser below does the same thing

parser = OptionParser()
parser.add_option('--loglevel', dest='loglevel', default='DEBUG',
    help='Logging verbosity')
parser.add_option('-s', '--server', dest='server', default='127.0.0.1',
    help='Server URL to connect')
parser.add_option('-p', '--port', dest='port', default='5000',
    help='Server port')
parser.add_option('--protocol', dest='protocol', default='json',
    help='Protocol used to communicate with server')
parser.add_option('-u', '--user', dest='username', default='anonymous',
    help='Username in server')
parser.add_option('-w', '--password', dest='password', default='',
    help='Password in server') # TODO: prompt, not pass directly in cmdline

if __name__ == '__main__':
    (options, args) = parser.parse_args()

    if 1:
        print options
        #p = ConfigParser.RawConfigParser(configdefaults)
        #p.write(open('teste.conf', 'w'))
    else:
        s = ConfigParser.RawConfigParser()
        s.read('teste.conf')
        print s.items('DEFAULT')

