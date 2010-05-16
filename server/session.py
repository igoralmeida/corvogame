# -*- coding: utf-8 -*-

from client_handler import ClientHandler
import traceback

class Session(ClientHandler):
  def __init__(self, unknown_connection):
    self.username = unknown_connection.username
    ClientHandler.__init__(self, unknown_connection.socket)
    self.message_handler = unknown_connection.message_handler 
 
  def write(self, message):
    ClientHandler.write(self, self.message_handler.to_string(message) + '\n')

 
  def handle_error(self):
    print "received an error, closing connection"
    traceback.print_exc()
    self.close()