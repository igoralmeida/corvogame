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
import logging
import asyncore, socket
from common import websocket_handler

class WebsocketListener(asyncore.dispatcher):
    ''' Basic TCP server. Handles new connections and send them to an UnknownConnectionHandler,
        later promoting it to active sessions'''
    def __init__(self, ip, port, server):
        logging.debug("Initializing websocket listener..")
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip,port))
        self.listen(5)
        self.server = server

    def handle_accept(self):
        ''' Handle an incomming connection and build a unknonw connection handler over it  '''
        try:
            conn,addr = self.accept()
            logging.info("Accepted {0} on address {1} ".format(conn, addr))

            data = conn.recv(255)

            if 'HTTP' in data:
                conn.send("HTTP/1.1 101 Web Socket Protocol Handshake\r\n"+"Upgrade: WebSocket\r\n"+"Connection: Upgrade\r\n"+"WebSocket-Origin: null\r\n" +"WebSocket-Location: "+" ws://192.168.1.136:1234/websession\r\n\r\n")

            self.server.promote_to_unknown_connection(conn, addr, websocket_handler.WebsocketHandler())

        except Exception, e:
            print "error accepting connection", e

    def shutdown(self):
        logging.debug("websocket listener is shutting down...")
