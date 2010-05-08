# -*- coding: utf-8 -*-

import asyncore, socket
import message
import simple_auth
import simple_reader
import client_handler

class UnknownConnectionHandler(client_handler.ClientHandler):
  def __init__(self, conn, server):
    client_handler.ClientHandler.__init__(self, conn)
    self.server = server
    self.write("Welcome to corvogame! Please input your protocol: ")
    self.read_handler = self._unknown_protocol_message
  
  def _unknown_protocol_message(self, data):
    prot_type = data.strip()

    if prot_type in self.server.message_handlers:
      print "promoting {1} to {0} protocol: ".format(prot_type, self.socket)
      self.read_handler = self._auth_handler
      self.message_handler = self.server.message_handlers[prot_type]
    else:
      self.write("Invalid protocol type: {0}\r\n".format(prot_type))
      self.shutdown()  
      
  def _auth_handler(self,data):
    readed, errors = self.message_handler(data)
    
    if readed:
      try:
	message = readed[0]
	assert message[u'action'] == 'logon'
	username = message[u'username']
	password = message[u'password']
	
	print "User {0} has logged with pasword {1}".format(username, password)
      except KeyError:
	self.write("Invalid logon message: {0}".format(readed[0]))
	self.shutdown()
  
  def handle_read(self):
    data = self.recv(8192)    
    self.read_handler(data) 
    
class ServerListener(asyncore.dispatcher):
  def __init__(self, ip, port):
    self.sessions = {}
    self.message_handlers = {}
    self.pending_sessions = {}
    self.auth_handler = None
    self.ip = ip
    self.port = port
    
    asyncore.dispatcher.__init__(self)    
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.set_reuse_addr()
    self.bind((ip,port))
    self.listen(5)
    
  def register_message_handler(self, protocol, handler):
    self.message_handlers[protocol] = handler
  
  def register_auth_handler(self, handler):
    self.auth_handler = handler
    
  def handle_accept(self):
    try:
      conn,addr = self.accept()
      print "accepted: ", conn, "on address:" , addr
      self.pending_sessions[addr] = UnknownConnectionHandler(conn, self)
    except Exception, e:
      print "error accepting connection", e
  
  def shutdown(self):
    pass
  
  def promote_to_session(self, unk_conn, protocol):
    pass
  
if __name__ == "__main__":
  server = ServerListener("0.0.0.0", 5000)
  
  server.register_auth_handler(simple_auth.authenticate)
  server.register_message_handler("json", simple_reader.read)
  
  try:
    asyncore.loop(timeout=4.0)
  except KeyboardInterrupt:
    print "Closing corvogame server"
    server.shutdown()
    print "done"