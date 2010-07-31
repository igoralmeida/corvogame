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
import time

logging.basicConfig(level=logging.INFO, format= '%(asctime)s %(levelname)-8s %(module)-20s[%(lineno)-3d] %(message)s')

class Client(ClientHandler):
    def __init__(self, ip, port, sock = None):
        ClientHandler.__init__(self)

        self.message_handler = Handler("\r\n")
        self.action_handlers = { "connection_response" : self.handle_connection_response , 'session_logon' : self.handle_session_logon, 'ping' : self.handle_ping, 'lobby_session_logon' : self.session_logon }
        self.read_handler = self.handle_message

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((ip , port))
        
    def session_logon(self, message):
        pass
        
    def handle_ping(self, message):
        if 'time' in message:
            before = float(message['time'])
            print 'response delay:', time.time() - before
        
    def handle_session_logon(self, message):
        if message['username'] == 'user':
            self.write({"action" : "lobby_chat" , 'message' : "oi mamae"})
            
    def handle_connection_response(self, message): 
        self.write({"action" : "login", "username" : "user", "password" : "123456"})
    
    def write(self, message):
        ClientHandler.write(self, self.message_handler.to_string(message))
        
    def handle_connect(self):
        logging.info("Connected!")
        self.send("json\r\n")
            
    def handle_message(self, message):
        logging.debug("handle_message: {0}".format(message))
        if message['action'] in self.action_handlers:            
            self.action_handlers[message['action']](message)
        else:
            pass#logging.info("Unhandled message: {0}".format(message))
        
if __name__ == "__main__":
    clients = []
    
    if len(sys.argv) < 4:
        print 'usage:', sys.argv[0], '[host] [port] [instances]'
        exit(1)
    
    for i in xrange(int(sys.argv[3])):
        clients.append(Client(sys.argv[1], int(sys.argv[2])))

    try:
        asyncore.loop(timeout=1.0)
    except KeyboardInterrupt:
        for cli in clients:
            cli.close()
