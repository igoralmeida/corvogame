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
from debug import debug
import lobby_handler
import asyncore
import socket
import logging

class Client(client_handler.ClientHandler):
    ''' Basic TCP client. '''
    def __init__(self, config, ui=None):
        logging.debug("Initializing Client...")
        client_handler.ClientHandler.__init__(self)

        self.config = config
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.ui = ui
        if ui is not None:
            ui.register_connection_handler(self)

        logging.debug("Connecting to server {0}:{1}".format(self.config.server, self.config.port))

        self.connect((self.config.server,int(self.config.port)))

        self.message_handlers = {}

    def signal_ui(self, message):
        if self.ui is not None:
            #TODO what to do here?
            pass

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
            message[u'accepted'] == u'yes'):

            self.read_handler = self.logon_response_handler
            #FIXME what if next msg==action:session_*?

            self.send_logon(self.config.username, self.config.password)

    def send_logon(self, user, passwd):
        """ Send logon information to server using credentials passed """
        logon_dict = { u'action' : 'login', u'username' : user, u'password' : passwd }
        self.write(self.message_handler.to_string(logon_dict))

    #TODO remove from this class
    def logon_response_handler(self, message):
        ''' Check if server acknowledges our authentication '''
        logging.debug("handling message: {0}".format(message))

        if message[u'action'] == u'logon_response':
            if message[u'authenticated'] == u'yes':
                logging.info("Successful authentication as {0}".format(self.config.username))
                self.handover_to_lobbyhandler()
            else:
                logging.error("Authentication failure for username '{0}' : {1}".format(self.config.username, message[u'result_text']))

                self.ui.require_logon()
                l, p = self.ui.get_logon()
                self.send_logon(l, p)

    def handover_to_lobbyhandler(self):
        self.lh = lobby_handler.LobbyHandler(sock=self.socket, cfg=self.config,
            msg_handler=self.message_handler, ui=self.ui)
        self.lh.inbuffer = self.inbuffer

    def shutdown(self):
        # FIXME if we were called too soon, there was no time to instantiate
        # LobbyHandler in handover_to_lobbyhandler and this will trigger an
        # exception.

        logging.debug("Client is shutting down...")
        self.lh.shutdown()
        logging.debug("done")

    def handle_connect(self):
        logging.debug("Connected sucessfully")
        self.read_handler = self.connection_response_handler
        self.write(self.config.protocol)
