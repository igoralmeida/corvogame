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

import asyncore, socket
import unknown_connection
import session
import logging

class ServerListener(asyncore.dispatcher):
    ''' Basic TCP server. Handles new connections and send them to an UnknownConnectionHandler,
        later promoting it to active sessions'''
    def __init__(self, ip, port):
        logging.debug("Initializing Serverlistener..")

        self.sessions = {}
        self.message_handlers = {}
        self.pending_sessions = {}
        self.logon_handler = None
        self.auth_handler = None
        self.ip = ip
        self.port = port

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip,port))
        self.listen(5)

    def register_logon_handler(self, logon_handler):
        logging.debug("Registering {0} as a logon handler".format(logon_handler))
        self.logon_handler = logon_handler

    def register_message_handler(self, protocol, handler):
        logging.debug("Registering {0} as a message handler".format(handler))
        ''' register's message handlers. Used to make the server abstract on how
            messages are parsed. '''
        self.message_handlers[protocol] = handler

    def register_auth_handler(self, handler):
        logging.debug("Registering {0} as a auth handler".format(handler))
        ''' register's authentication handlers. Used to make the server abstract on how
            messages are parsed. '''
        self.auth_handler = handler

    def handle_accept(self):
        ''' Handle an incomming connection and build a unknonw connection handler over it  '''
        try:
            conn,addr = self.accept()
            logging.info("Accepted {0} on address {1} ".format(conn, addr))
            self.pending_sessions[addr] = unknown_connection.UnknownConnectionHandler(conn, self, addr)
        except Exception, e:
            print "error accepting connection", e

    def shutdown(self):
        logging.debug("server listener is shutting down...")

    def promote_to_unknown_connection(self, conn, addr, handler = None):
        uc = unknown_connection.UnknownConnectionHandler(conn, self, addr)
        self.pending_sessions[addr] = uc
        if handler:
            uc.upgrade_protocol_handler(handler)

    def promote_to_session(self, unknown_connection, protocol, address):
        logging.debug("Promoting {0} to a session".format(unknown_connection))
        s = session.Session(unknown_connection)

        del self.pending_sessions[address]
        if self.logon_handler:
            logging.debug("Calling logon handler")
            self.logon_handler(s)
