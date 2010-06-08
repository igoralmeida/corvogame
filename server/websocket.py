# -*- coding: utf-8 -*-
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
