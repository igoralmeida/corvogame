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
import threading

logging.basicConfig(level=logging.INFO, format= '%(asctime)s %(levelname)-8s %(module)-20s[%(lineno)-3d] %(message)s')

class Client(ClientHandler):
    LOBBY = 0
    GAME_LOBBY = 1
    IN_GAME = 2
    
    def __init__(self, ip, port, sock = None):
        ClientHandler.__init__(self)

        self.message_handler = Handler("\r\n")
        self.action_handlers = { "connection_response" : self.handle_connection_response , 
                                 'session_logon' : self.handle_session_logon, 
                                 'ping' : self.handle_ping, 
                                 'lobby_session_logon' : self.session_logon,
                                 'lobby_info' : self.handle_lobby_info,
                                 'logon_response' : self.handle_session_logon,
                                 'lobby_create_game' : self.handle_game_create,
                                 'wargame_handshake' : self.handle_wargame_handshake }

        lobby_actions = [ ('say something' , { 'action' : 'lobby_chat', 'fields' : [ ('message', str, True) ] }),
                          ('create game' , { 'action' : 'lobby_create_game', 'fields' : [('game_type', str, True), ('room_name', str, True) ] } ),
                          ('join game', { 'action' : 'lobby_join_game' , 'fields' : [('room_id', str, True) ] } )  ]
        
        game_lobby_actions  = [ ('say something' , { 'action' : 'wargame_lobby_chat', 'fields' : [ ('message', str, True) ] }),
                                ('change color', { 'action' : 'wargame_lobby_set_self_color', 'fields' : [ ('color', str, True) ] } ),
                                ('set ready' , { 'action' : 'wargame_lobby_set_self_ready', 'fields' : [ ('ready', str, True) ] }),
                                ('start game', { 'action' : 'wargame_lobby_start_game' , 'fields' : [] } )]
        
        in_game_actions = [ ('remove a piece', {'action' : 'wargame_remove_piece', 'fields' : [ ('from', str, True) ] } ),
                            ('add a piece', {'action' : 'wargame_add_piece', 'fields' : [ ('to', str, True) ] } ),
                            ('say something' , { 'action' : 'wargame_chat', 'fields' : [ ('message', str, True ) ] } ),
                            ('attack a land', {'action' : 'wargame_attack_land', 'fields' : [ ('quantity', str, True), ('from', str, True), ('to', str, True) ] } ),
                            ('end turn' , { 'action' : 'wargame_end_turn', 'fields' : [] }  ) ]                                               
        
        self.menu = [ lobby_actions, game_lobby_actions, in_game_actions ]
        
        self.current_state = self.LOBBY
        
        self.read_handler = self.handle_message

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((ip , port))
        
        self.showing_menu = False
                
    def print_menu(self):
      def respawn():
        threading.Timer(0.01, self.print_menu).start()
      
      if self.showing_menu:
        return
      
      self.showing_menu = True
      
      i = 0
      for item in self.menu[self.current_state]:
        print "{0} - {1}".format(i, item[0])
        i += 1
      
      value = raw_input("select a value: ")
      params = {}
      
      try:
        value = int(value)
      except:
        print 'Error: invalid format for menu value'
        respawn()
        return
      
      if value > len(self.menu[self.current_state]):
        print ' invalid value {0}.'.format(value)
        respawn()
        return
      
      reqd = { True : ' (required) ', False : ' (enter to proceed) ' }
      for param in self.menu[self.current_state][value][1]['fields']:
        item_value = raw_input('{0}{1}: '.format(param[0], reqd[param[2]]))        
        params[param[0]] = param[1](item_value)
      
      message = params
      message['action'] = self.menu[self.current_state][value][1]['action']
      
      self.write(message)
      
      self.showing_menu = False
      
    def session_logon(self, message):
      print "session {0} logged.".format(message['username'])
    
    def handle_lobby_info(self, message):
      print 'received lobby info. :', message
      
    def handle_ping(self, message):
        if 'time' in message:
            before = float(message['time'])
            print 'response delay:', time.time() - before

    def handle_game_create(self, message):
      if message['status'] == 'sucessfull':
        self.current_state = self.GAME_LOBBY
      else:
        print 'error creating game: ', message
      
    def handle_wargame_handshake(self, message):
        self.current_state = self.IN_GAME
        
    def handle_session_logon(self, message):
        print 'received seession logon response: ', message
        if message['authenticated'] == 'yes':
            print 'authenticated'
            
    def handle_connection_response(self, message): 
        print 'received connection response: ', message
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
            print "Unhandled message: {0}".format(message)
        
        if not self.showing_menu:
          threading.Timer(0.01, self.print_menu).start()
        
if __name__ == "__main__":
    clients = []
    
    if len(sys.argv) < 4:
        print 'usage:', sys.argv[0], '[host] [port] [instances]'
        exit(1)
    
    for i in xrange(int(sys.argv[3])):
        clients.append(Client(sys.argv[1], int(sys.argv[2])))

    try:
        asyncore.loop(timeout=0.001)
    except KeyboardInterrupt:
        for cli in clients:
            cli.close()
