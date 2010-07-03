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
import logging
from optparse import OptionParser

configurables = ['loglevel','server','port','protocol','username','password']

configdefaults = {
    'loglevel': 'DEBUG',
    'server': '127.0.0.1',
    'port': '5000',
    'protocol': 'json',
    'username': 'anonymous',
    'password': '',
}

class Config():
    ''' Configuration directory. Centralizes all necessary information
    configurable by the user.
    Instance variables are Config.{loglevel,server,port...}, as listed in
    "configurables" global'''

    def __init__(self):

        parser = OptionParser()
        parser.add_option('--loglevel', dest='loglevel', default='DEBUG',
            help='Logging verbosity')
        parser.add_option('-s', '--server', dest='server', default='127.0.0.1',
            help='Server URL to connect')
        parser.add_option('-p', '--port', dest='port', type='int', default='5000',
            help='Server port')
        parser.add_option('--protocol', dest='protocol', default='json',
            help='Protocol used to communicate with server')
        parser.add_option('-u', '--user', dest='username', default='anonymous',
            help='Username in server')
        parser.add_option('-w', '--password', dest='password', default='',
            help='Password in server') # TODO: prompt, not pass directly in cmdline
        parser.add_option('-c', '--configfile', dest='configfile', default='corvogame.conf',
            help='Configuration file')
        (opt, args) = parser.parse_args()

        # Be able to use Config.loglevel, Config.server, etc.
        self.__dict__.update(opt.__dict__)

        self.cp = ConfigParser.RawConfigParser()
        self.cp.read(opt.configfile)

        self.diff = [(key, opt.__dict__[key]) for key in self.cp._defaults.keys()
            if str(opt.__dict__[key]) != self.cp._defaults[key]]

        if __name__ != '__main__':
            self.update()

    def update(self):
        ''' Update Config.server, Config.loglevel, etc., from ConfigParser '''
        self.__dict__.update(self.cp._defaults)

    def reset(self):
        ''' Overwrite configfile with default values '''

        self.cp = ConfigParser.RawConfigParser(configdefaults)
        logging.info('Resetting configuration file')
        self.cp.write(open(self.configfile, 'w'))

    def save_diff(self):
        ''' Update ConfigParser with new configurations from command-line '''
        if self.diff.__len__() > 0:
            for k,v in self.diff:
                self.cp.set('DEFAULT', k, v)
            self.update()

    def write(self, filename=''):
        if filename is '':
            filename = self.configfile

        self.cp.write(open(filename, 'w'))

    def __setattr__(self, name, value):
        if name in configurables:
            #TODO check for sanity and update config file
            pass
        else:
            self.__dict__[name] = value

if __name__ == '__main__':
    c = Config()
    c.save_diff()
    c.write()
