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

from common import client_handler
import config
import asyncore
import socket
import logging

def debug(s):
    logging.debug("--------------- Read from socket:")
    logging.debug(s)

class Client(client_handler.ClientHandler):
    ''' Basic TCP client. '''
    def __init__(self, ip=None, port=None):
        client_handler.ClientHandler.__init__(self)
        logging.debug("Initializing Client...")

        self.Cfg = config.Config()

        self.message_handlers = {}

        self.ip = ip
        if ip is None:
            self.ip = self.Cfg.server

        self.port = port
        if port is None:
            self.port = int(self.Cfg.port) # may come from ConfigParser

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.ip,self.port))

    def register_message_handler(self, protocol, handler):
        ''' Register message handlers. Used to make the client abstract on how
            messages are parsed. '''
        logging.debug("Registering {0} as a message handler".format(handler))
        self.message_handlers[protocol] = handler
        self.message_handler = handler

    #TODO remove from this class
    def connection_response_handler(self, message):
        ''' Continue conversation: if protocol is accepted, send login info. '''
        #TODO implement fallback to some other protocol if not accepted

        if (message[u'action'] == u'connection_response' and
            message[u'result'].startswith('Protocol accepted.')):
            self.read_handler = self.logon_response_handler
            #FIXME what if next msg==action:session_*?

            logon_dict = { u'action' : 'login', u'username' : self.Cfg.username, u'password' : self.Cfg.password }
            logon_message = self.message_handler.to_string(logon_dict)
            self.write(logon_message)

    #TODO remove from this class
    def logon_response_handler(self, message):
        ''' Check if server acknowledges our authentication '''

        if message[u'action'] == u'logon_response':
            if message[u'result'] == u'connected successfully':
                logging.info("Successful authentication as {0}".format(self.Cfg.username))
                self.read_handler = debug
            else:
                #TODO ask for login information again
                pass

    def shutdown(self):
        logging.debug("Client is shutting down...")

    def handle_connect(self):
        self.read_handler = self.connection_response_handler
        self.write(self.Cfg.protocol)

