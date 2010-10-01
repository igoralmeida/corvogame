# -*- coding: utf-8 -*-
from common import broadcastable
import logging
import utils
import copy
import war

class WargameLobby(broadcastable.Broadcastable):
  COLORS = ['red','blue','black','green','yellow','white']
  
  def __init__(self, main_lobby, room_owner, room_configuration, game_id):
    logging.debug("Initializing wargame internal lobby")
    
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
    self.available_colors = copy.copy(self.COLORS)
    
    self.start()
  
  def handle_set_self_ready(self, session, message):
    if utils.validate_message(message, session, ['ready']) \
      and utils.validate_field_values(message, session, 'ready', message['ready'], ['true','false']):
      
      session['ready'] = message['ready'] == 'true'
      
      self.broadcast({ 'session' : 'game_lobby' }, { 'action' : 'game_lobby_player_ready_state', \
                                                     'ready' : message['ready'], 'username' : session.username } )

  def send_handshake(self, session):
    session.write( { 'action': 'lobby_game_capabilities' , 
                     'capabilities' : self.capabilities,
                     'available_colors' : self.available_colors })
    
  def handle_set_self_color(self, session, message):
    if not utils.validate_message(message, session, [ 'color' ]):
      return
    
    logging.debug("Trying to set color [{0}] to user [{1}]".format(message['color'], session.username))
    

    if message['color'] not in self.available_colors:
      logging.debug("User provided an invalid or taken color")
      session.write({'action' : 'lobby_set_self_color', 'status' : 'error', 'reason' : 'invalid or already taken color {0}'.format(message['color'])})
      return
    elif 'self_color' in session:
      logging.debug("User already have a color [{0}] defined, removing it and trying to define the new color".format(session['self_color']))
      self.available_colors.append(session['self_color'])
      session['self_color'] = message['color']
      self.available_colors.remove(message['color'])
    else:
      logging.debug("Setting color [{0}] to user. Available colors: {1}".format(message['color'], self.available_colors))
      session['self_color'] = message['color']
      self.available_colors.remove(message['color'])
    
    self.broadcast( { 'session' : 'game_lobby' }, { 'action' : 'lobby_player_updated_color', 'username' : session.username,  'color' : message['color'] })
    self.broadcast( { 'session' : 'game_lobby' }, { 'action' : 'lobby_available_colors', 'colors' : self.available_colors })
    
  def handle_send_lobby_chat(self, session, message):
    logging.debug("Handling chat message")
    message["action"] = u'lobby_chat'
    message["sender"] = session.username

    self.broadcast(session, message)
    
  def handle_session_disconnect(self, session):
    logging.debug("Handling session disconnect")

    self.remove_from_broadcast(session)
    
    logging.debug("{0}".format(self.lobby_sessions))
    
    if session in self.lobby_sessions:
        self.lobby_sessions.remove(session)

    msg = { u'action' : 'lobby_session_logout', u'username' : session.username , u'user_id' : session.user_id }
    self.broadcast({u'session' : 'lobby'} , msg)
  
  def add_session(self, session, logon_message):
    if len(self.lobby_sessions) >= war.MAX_PLAYERS:
      session.write( { 'action' : 'lobby_join', 'status' : 'error' , 'reason' : 'Max players reached :(' })
      return False

    session.incoming_message_handler = self.on_session_message
    session.close_handler = self.handle_session_disconnect
    session['self_color'] = self.available_colors.pop()
    
    self.lobby_sessions.append(session)
    self.send_handshake(session)
    self.add_to_broadcast(session)
    
    return True
    
  def on_session_message(self, session, message):
      logging.debug("Received message {0} from user {1}".format(message, session.username))
      if message["action"] in self.message_handlers:
          self.message_handlers[message["action"]](session, message)