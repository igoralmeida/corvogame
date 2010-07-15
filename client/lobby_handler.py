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

from common import client_handler
from debug import debug
import config
import asyncore
import logging

class LobbyHandler(client_handler.ClientHandler):
    ''' Lobby-level message parser.

    Uses connection from client_connection.Client and syncs user/room
    information with lobby on server
    '''

    def __init__(self, sock, cfg, msg_handler, ui=None):
        client_handler.ClientHandler.__init__(self, sock)
        logging.debug("Initializing LobbyHandler...")

        self.Cfg = cfg

        self.message_handler = msg_handler
        self.read_handler = self.lobby_parse

        self.ui = ui
        if ui is not None:
            self.ui.register_connection_handler(self)

        self.rooms = []
        self.users = {} #{'name':{username:'name',...}, 'name2':...}

    def common_parse(self, message):
        if message[u'action'].startswith('session_'):
            action = message[u'action'][8:] #remove 'session_' from string

            {
                'logon': self.logon_bcast,
                'logout': self.logout_bcast,
            }[action](message[u'username'])

    def logon_bcast(self, user):
        self.add_user(user)
        self.signal_ui({u'action': 'logon', u'user': user})
        logging.info('User {0} logs in'.format(user))

    def logout_bcast(self, user):
        self.remove_user(user)
        self.signal_ui({u'action': 'logosut', u'user': user})
        logging.info('User logs out'.format(user))

    def lobby_parse(self, message):
        if message[u'action'] == u'lobby_info':
            newrooms = [r for r in message[u'rooms'] if r not in self.rooms]
            self.rooms.append(newrooms)
            self.update_users(message[u'users'])

        self.read_handler = self.common_parse

    def chat_send(self, text):
        # TODO entender a mensagem de chat no lobby
        message = { u'action': 'chat', u'text': text }
        pass

    def signal_ui(self, message):
        if self.ui is not None:
            if message[u'action'] == u'chat':
                self.ui.chat_received(message)
            elif message[u'action'] == u'logon':
                self.ui.user_logon(message[u'user'])
            elif message[u'action'] == u'logout':
                self.ui.user_logout(message[u'user'])

    def update_users(self, user_dicts):
        for i in user_dicts:
            if i[u'username'] not in self.users:
                self.users.update({i[u'username']: i})

    def add_user(self, name):
        if name not in self.users:
            self.users.update({name: {u'username': name}})

    def remove_user(self, name):
        if name in self.users:
            del self.users[name]
