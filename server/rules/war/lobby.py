# -*- coding: utf-8 -*-
import broadcastable
import war
import logging

class WargameLobby(broadcastable.Broadcastable):
  COLORS = ['red','blue','black','green','yellow','white']
  
  def __init__(self, main_lobby, room_owner, room_configuration, game_id):
    broadcastable.Broadcastable.__init__(self)
    self.lobby_sessions = []
    self.main_lobby = main_lobby
    self.room_owner = room_owner
    self.room_name = room_configuration['room_name']
    self.game_id = game_id
    self.message_handlers = { 'lobby_chat' : self.handle_send_lobby_chat,
                              'lobby_set_self_color' : self.handle_set_self_color, 
                              'lobby_set_self_ready' : self.handle_set_self_ready }
    
    self.capabilities = [ 'can_set_self_color' ]   
    self.available_colors = ['red','blue','black','green','yellow','white']
    
    self.start()
  
  def handle_set_self_ready(self, session, message):
    pass
    
  def send_handshake(self, session):
    session.write( { 'action': 'lobby_game_capabilities' , 
                    'capabilities' : self.capabilities,
                    'available_colors' : self.available_colors })
    
  def handle_set_self_color(self, session, message):
    if 'self_color' in session:
      self.colors.append(session['self_color'])
      session['self_color'] = message['color']
    elif message['color'] not in self.COLORS:
      session.send({'action' : 'lobby_set_self_color', 'status' : 'error', 'reason' : 'invalid color {0}'.format(message['color'])})
      return
    else:
      session['self_color'] = message['color']
      self.available_colors = self.available_colors.remove(message['color'])
      
    session.send({ 'action' : 'lobby_set_self_color', 'status' : 'ok' })
    self.broadcast( { 'session' : 'game_lobby' }, { 'action' : 'lobby_player_update_color', 'color' : message['color'] })
    
  def handle_send_lobby_chat(self, session, message):
    logging.debug("Handling chat message")
    message["action"] = u'lobby_chat'
    message["sender"] = session.username

    self.broadcast(session, message)
    
  def handle_session_disconnect(self, session):
    pass
  
  def add_session(self, session, logon_message):
    if len(self.lobby_sessions) >= war.MAX_PLAYERS:
      session.write( { 'action' : 'lobby_join', 'status' : 'error' , 'reason' : 'Max players reached :(' })
      return False

    session.incoming_message_handler = self.on_session_message
    session.close_handler = self.handle_session_disconnect
    
    self.lobby_sessions.append(session)
    self.send_handshake(session)
    self.add_to_broadcast(session)
    
    return True
    
  def on_session_message(self, session, message):
      logging.debug("Received message {0} from user {1}".format(message, session.username))
      if message["action"] in self.handlers:
          self.handlers[message["action"]](session, message)