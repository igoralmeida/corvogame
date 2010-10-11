# -*- coding: utf-8 -*-

import logging
from common import broadcastable
import uuid
import utils

class Lobby(broadcastable.Broadcastable):
    def __init__(self):
        logging.debug("Initializing lobby")
        broadcastable.Broadcastable.__init__(self)

        self.sessions = {}
        self.channels = {}
        self.games = {}
        self.game_builders = {}

        self.handlers =  { 'lobby_chat' : self.handle_chat ,
                           'lobby_quit' : self.handle_session_quit,
                           'lobby_join_game' : self.handle_join_game,
                           'lobby_create_game' : self.handle_create_game }
        self.start()

    def handle_join_game(self, session, message):
        if 'id' in message['room_id'] and message['room_id'] in self.games:
          self.games.add_session(session)          

    def handle_create_game(self, session, message):
        if utils.validate_message(message, session, [ 'game_type', 'room_name' ]):
          if not message['game_type'] in self.game_builders:
            session.write({ 'action' : message['action'], 'status' : 'reject', 'reason' : 'invalid game type : ' + message['game_type'] })
            return
          
          if not len(message['room_name']) > 3:
            session.write({ 'action' : message['action'], 'status' : 'reject', 'reason' : 'room name too small' })
            return
            
          game_id = uuid.uuid1().get_hex()
          
          logging.info("Session {0} is trying to create a game of type {1} and room name of {2}".format(session.username , message['game_type'], message['room_name']))
          game_lobby = self.game_builders[message['game_type']].build_lobby(main_lobby=self, room_owner=session, room_configuration= message, game_id=game_id)
          
          self.games[game_id]  = game_lobby
          
          logging.info("Created sucessfully")
          game_lobby.add_session(session, None)
          self.remove_from_broadcast(session)
          
          del self.sessions[session.username]
          
          
          session.write({ 'action' : 'lobby_create_game', 'status' : 'sucessfull', 'game_id' : game_id  })
          self.broadcast({ u'session' : 'lobby' }, { 'action' : 'lobby_game_created', 
                                                     'room_name' : message['room_name'], 
                                                     'username': session.username, 
                                                     'game_type' : message['game_type'] })
          
    def handle_session_disconnect(self, session):
        logging.debug("Handling session disconnect")

        self.remove_from_broadcast(session)

        if session.username in self.sessions:
            del self.sessions[session.username]

        msg = { u'action' : 'lobby_session_logout', u'username' : session.username , u'user_id' : session.user_id }
        self.broadcast({u'session' : 'lobby'} , msg)

    def handle_session_quit(self, session, message):
        logging.debug("Handling session quit")

        self.remove_from_broadcast(session)
        if session.username in self.sessions:
            del self.sessions[session.username]

        msg = { u'action' : 'lobby_session_logout', u'username' : session.username , u'user_id' : session.user_id }
        self.broadcast({u'session' : 'lobby'} , msg)

        session.shutdown()

    def add_game(self, name, game_factory):
        if name not in self.games:
            self.game_builders[name] = game_factory

    def handle_chat(self, session, message):
        logging.debug("Handling chat message")
        if utils.validate_message(message, session, [ 'message' ]):
          message["sender"] = session.username
          self.broadcast(session, message)

    def get_rooms(self):
        logging.debug("Getting rooms")
        return []

    def get_users(self):
        logging.debug("Getting users")
        users = []

        for username in self.sessions:
            user_msg = {}
            user_msg[u'username'] = username
            user_msg[u'user_id'] = self.sessions[username].user_id
            users.append(user_msg)

        return users

    def stop(self):
        broadcastable.Broadcastable.stop(self)
        
        map(lambda x: x.shutdown(), self.sessions.values())        
        self.sessions.clear()
        self.handlers.clear()
        
    def get_game_builders(self):
        ret = []
        for game in self.game_builders:
            logging.debug("Getting game builder for game {0}".format(game))
            g = {}
            g["name"] = game
            g["description"] = self.game_builders[game].DESCRIPTION
            g["player_count"] = self.game_builders[game].MAX_PLAYERS
            g["version"] = self.game_builders[game].VERSION
            g["author"] = self.game_builders[game].AUTHOR

            ret.append(g)

        return ret

    def handshake(self, session):
        logging.debug("Doing handshake for username {0}".format(session.username))
        session.incoming_message_handler = self.on_session_message
        session.close_handler = self.handle_session_disconnect

        message = {}
        message["action"] = "lobby_info"
        message["rooms"] = self.get_rooms()
        message["users"] = self.get_users()
        message["available_games"] = self.get_game_builders()
        session.write(message)

        self.add_to_broadcast(session)
        self.broadcast( { u'session' : 'lobby'} , { u'action' : 'lobby_session_logon', u'username' : session.username, u'user_id' : session.user_id })
        self.sessions[session.username] = session

    def on_session_message(self, session, message):
        logging.debug("Received message {0} from user {1}".format(message, session.username))
        if message["action"] in self.handlers:
            self.handlers[message["action"]](session, message)
