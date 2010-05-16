# -*- coding: utf-8 -*-

import client_handler

class RawHandler(object):
  def from_string(self, raw_string):
    data = raw_string.strip()
    return (True, [data], "")
  
  def to_string(self,message):
    pass
  
class UnknownConnectionHandler(client_handler.ClientHandler):
  ''' Class handler for an unknown source connection
  
  We define as unknown connection a client that has not made a initial handshake:
  before we determine the message protocol and authentication steps.
  '''
  
  def __init__(self, conn, server, addr):
    ''' Starts the handler and define the read method as 'not protocol enabled yet' '''
    client_handler.ClientHandler.__init__(self, conn)
    self.server = server
    self.write("Welcome to corvogame! Please input your protocol: ")
    self.read_handler = self._unknown_protocol_message
    self.message_handler = RawHandler()
    self.addr = addr
       
  def _unknown_protocol_message(self, data):
    ''' handshake handler. basically it checks if the client has inputted an
	valid protocol_handler. Otherwise, disconnects '''

    if data in self.server.message_handlers:
      print "promoting {1} to {0} protocol: ".format(data, self.socket)
      self.read_handler = self._auth_handler
      self.message_handler = self.server.message_handlers[data]
    else:
      self.write("Invalid protocol type: {0}\r\n".format(data))
      self.shutdown()  
  
  def handle_error(self):
      print "shit"
      
  def _auth_handler(self, message):
    ''' after promoted as an protocol enabled connection, waits for an logon message,
	and give it to the auth_handler to check if something gone wrong. If yes,
	disconnects, otherwise notify the server to a new session '''	
 
    try:
      assert message[u'action'] == 'logon'
      username = message[u'username']
      password = message[u'password']
      
      print "Trying to authenticate [%s]" % username
      
      if self.server.auth_handler(message):
	self.username = username
	self.server.promote_to_session(self, self.message_handler, self.addr)
	  
    except KeyError:
      self.write("Invalid logon message: {0}".format(readed[0]))
      self.shutdown()
    