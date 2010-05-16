# -*- coding: utf-8 -*-

import threading

class Lobby(threading.Thread):
  def __init__(self):
    self.sessions = {}
    self.channels = {}
    self.message_pump = []   
    self.pump_lock = threading.Condition()
  
  def get_rooms(self):
    return []
  
  def get_users(self):
    return []
  
  def handshake(self, session):
    print "Doing handshake for username {0}".format(session.username)
    
    message = {}
    message["action"] = "lobby"
    message["rooms"] = self.get_rooms()
    message["users"] = self.get_users()
    
    session.write(message)
    print "doing some handshake"
    self.sessions[session.username] = session
    session.incoming_message_handler = self.on_session_message
  
  def on_session_message(self, session, message):
    if message["action"] == "chat":
      self.broadcast(message)
      
  def broadcast(self, from_session, message):
    self.pump_lock.acquire()
    self.message_pump.append(message)    
    self.pump_lock.notify()
  
  def run(self):
    while not self.message_pump:
      self.pump_lock.wait()
    
      message = self.message_pump.pop()    
      for user,session in self.sessions:
	session.write(message)