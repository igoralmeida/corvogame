# -*- coding: utf-8 -*-
'''
Created on 25/06/2010

@author: Victor Vicente de Carvalho
'''
import sys

sys.path.append('..')

from common.client_handler import ClientHandler
import socket
import asyncore
from common.json_handler import Handler
import logging

logging.basicConfig(level=logging.INFO, format= '%(asctime)s %(levelname)-8s %(module)-20s[%(lineno)-3d] %(message)s')

class Client(ClientHandler):
    def __init__(self, socket):        
        ClientHandler.__init__(self, socket)
                
        self.message_handler = Handler("\r\n")
        self.action_handlers = { "connection_response" : self.handle_connection_response , 'session_logon' : self.handle_session_logon}
        self.read_handler = self.handle_message

        self.send("json\r\n")
        
    def handle_session_logon(self, message):
        if message['username'] == 'user':
            self.write({"action" : "lobby_chat" , 'message' : "oi mamae"})
            
    def handle_connection_response(self, message): 
        self.write({"action" : "login", "username" : "user", "password" : "123456"})
    
    def write(self, message):
        ClientHandler.write(self, self.message_handler.to_string(message))
        
    def handle_connect(self):
        print "connected!"
        self.send("json\r\n")
    
    def handle_message(self, message):
        logging.debug("handle_message: {0}".format(message))
        if message['action'] in self.action_handlers:            
            self.action_handlers[message['action']](message)
        else:
            logging.info("Unhandled message: {0}".format(message))
            
if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sys.argv[1],5000))
    cli = Client(sock)
    
    try:
        asyncore.loop(timeout=1.0)
    except KeyboardInterrupt:
        cli.close()