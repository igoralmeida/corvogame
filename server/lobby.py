# -*- coding: utf-8 -*-

import logging
import broadcastable

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
                           'lobby_create_room' : self.handle_create_room }
        self.start()

    def handle_join_game(self, session, message):
        pass

    def handle_create_game(self, session, message):
        pass


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

    def handle_create_room(self, session, message):
        pass

    def add_game(self, name, game_factory):
        if name not in self.games:
            self.game_builders[name] = game_factory

    def handle_chat(self, session, message):
        logging.debug("Handling chat message")
        message["action"] = u'lobby_chat'
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
