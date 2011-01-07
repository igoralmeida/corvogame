# -*- coding: utf-8 -*-
#    This file is part of corvogame.
#
#    corvogame is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    corvogame is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with corvogame.  If not, see <http://www.gnu.org/licenses/>.

import ui_messages

import logging

class LobbyHandler():
    ''' Lobby-level message parser.

    Syncs user/room information with lobby on server
    '''

    def __init__(self, cfg, msg_sender, ui=None):
        logging.debug("Initializing LobbyHandler...")

        self.Cfg = cfg

        self.read_handler = self.common_parse
        self.msg_sender = msg_sender

        self.ui = ui
        if ui is not None:
            self.ui.register_connection_handler(self)

        self.rooms = []
        self.users = {} #{'name':{username:'name',...}, 'name2':...}
        self.gametypes = []

    def common_parse(self, message):
        if message[u'action'].startswith('lobby_'):
            action = message[u'action'][6:] #remove 'lobby_' from string

            {
                'session_logon': self.logon_bcast,
                'session_logout': self.logout_bcast,
                'chat': self.chat_received,
                'game_created': self.game_created,
                'info': self.info_parser,
                'create_game': self.game_creation_response,
            }[action](message)
        elif message[u'action'] == u'ping':
            #TODO would respond with pong, but handler is missing in server
            pass

    def logon_bcast(self, message):
        user = message[u'username']
        uid = message[u'user_id']
        self.add_user(user, uid)
        self.signal_ui(ui_messages.logon(user))
        logging.info('User {0} logs in'.format(user))

    def logout_bcast(self, message):
        user = message[u'username']
        self.remove_user(user)
        self.signal_ui(ui_messages.logout(user))
        logging.info('User logs out'.format(user))

    def game_creation_response(self, message):
        """ Our game request has been answered

        FIXME
        With the current design, we have 2 choices:
            * Handover to yet another class, say, WargameHandler, at the time of
            game request and risk being handover'ed back to LobbyHandler if our
            game lobby was rejected

            * Use this method to parse the game creation response, handover to
            WargameHandler in case we were accepted, but risk having to parse
            early action:wargame_lobby_* messages here in LobbyHandler if they
            come before the handover is done

        Since there is no way to re-insert messages in the queue, i'm going with
        the second. BUT THIS NEEDS TO BE FUCKING FIXED: create a know-it-all
        Client class which delivers to many xxxxHandler classes based on
        msg[u'action'].startswith
        """

        status = message[u'status']

        if status == 'successful':
            logging.info('Game creation has been accepted')
            info = message[u'game_id']
            logging.debug('Would perform handover to xxxxgameHandler')
            #TODO implement this
            #self.handover_to_gamehandler()

        elif message[u'status'] == 'rejected':
            info = message[u'reason']
            logging.info('Game creation has been rejected: {0}'.format(
                info))
            self.signal_ui(ui_messages.enable_chat())

        self.signal_ui(ui_messages.game_creation_response(status,info))

    def game_created(self, message):
        """ Someone has created a game """
        game = message.copy()
        del game[u'action']

        #FIXME should look for inconsistencies
        self.rooms.append(game)

        self.signal_ui(ui_messages.game_created(user=game[u'username'],
            game_type=game[u'game_type'], room_name=game[u'room_name']))

    def info_parser(self, message):
        newrooms = [r for r in message[u'rooms'] if r not in self.rooms]
        self.rooms.extend(newrooms)
        self.gametypes.extend(message[u'available_games']) #FIXME must update properly
        self.update_users(message[u'users'])

        self.signal_ui(ui_messages.user_list(self.users))
        self.signal_ui(ui_messages.room_list(self.rooms))
        self.signal_ui(ui_messages.enable_chat())

    def chat_received(self, message):
        sender = message[u'sender']
        text = message[u'message']

        self.signal_ui(ui_messages.chat_received(sender, text))

    def chat_send(self, text):
        message = { u'action': 'lobby_chat', u'message': text }
        self.msg_sender(message)

    def create_game(self, game_type, room_name):
        message = {u'action': 'lobby_create_game', u'game_type': game_type, u'room_name': room_name}
        self.msg_sender(message)

    def join_game(self, room_id):
        if room_id.__len__() != 32:
            logging.error('Bad room id hash: {0}'.format(room_id))
        else:
            message = {u'action': 'lobby_join_game', u'room_id': room_id}
            self.msg_sender(message)

    def ui_responder(self, msg):
        """ Centralizes the queries coming from the UI. """

        if msg[u'action'] == 'request':
            if msg[u'value'] == 'rooms':
                return self.rooms
            elif msg[u'value'] == 'users':
                return self.users
            elif msg[u'value'] == 'gametypes':
                return self.gametypes
        elif msg[u'action'] == 'create_game':
            if msg[u'game_type'] in [g[u'name'] for g in self.gametypes]:
                self.create_game(
                    game_type=msg[u'game_type'],
                    room_name=msg[u'room_name']
                )
            else:
                #TODO notify the UI
                pass
        elif msg[u'action'] == 'join_game':
            self.join_game(msg[u'room_id'])

    def signal_ui(self, message):
        if self.ui is not None:
            if message[u'action'] == u'chat':
                self.ui.chat_received(message)
            elif message[u'action'] == u'logon':
                self.ui.user_logon_event(message[u'user'])
            elif message[u'action'] == u'logout':
                self.ui.user_logout_event(message[u'user'])
            elif message[u'action'] == u'enable_chat':
                self.ui.enable_chat()
            elif (message[u'action'] == u'user_list' or
                    message[u'action'] == u'room_list'):
                self.ui.list_update(message[u'dicts'])
            elif message[u'action'] == 'game_created':
                game = message.copy()
                del game[u'action']
                self.ui.game_created(game)
            elif message[u'action'] == 'game_creation_response':
                self.ui.game_creation_response(message)

    def update_users(self, user_dicts):
        for i in user_dicts:
            if i[u'username'] not in self.users:
                self.users.update({i[u'username']: i})

    def add_user(self, name, uid):
        #TODO must check if user_id is incoherent
        if name not in self.users:
            self.users.update({name: {u'username': name, u'user_id': uid}})

    def remove_user(self, name):
        if name in self.users:
            del self.users[name]
