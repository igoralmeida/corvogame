# -*- coding: utf-8 -*-

import asyncore, socket
import unknown_connection
import session
   
class ServerListener(asyncore.dispatcher):
  ''' Basic TCP server. Handles new connections and send them to an UnknownConnectionHandler,
      later promoting it to active sessions'''
  def __init__(self, ip, port):
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
    self.logon_handler = logon_handler
    
  def register_message_handler(self, protocol, handler):
    ''' register's message handlers. Used to make the server abstract on how
	messages are parsed. '''
    self.message_handlers[protocol] = handler
  
  def register_auth_handler(self, handler):
    ''' register's authentication handlers. Used to make the server abstract on how
	messages are parsed. '''
    self.auth_handler = handler
    
  def handle_accept(self):
    ''' Handle an incomming connection and build a unknonw connection handler over it  '''
    try:
      conn,addr = self.accept()
      print "accepted: ", conn, "on address:" , addr
      self.pending_sessions[addr] = unknown_connection.UnknownConnectionHandler(conn, self, addr)
    except Exception, e:
      print "error accepting connection", e
  
  def shutdown(self):
    pass
  
  def promote_to_session(self, unknown_connection, protocol, address):
    print "Promoting {0} to a session".format(unknown_connection)
    s = session.Session(unknown_connection)
      
    del self.pending_sessions[address]   
    print "Calling logon handler"
    if self.logon_handler:
      self.logon_handler(s)