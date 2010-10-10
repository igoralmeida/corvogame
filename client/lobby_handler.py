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
import ui_messages

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
        if message[u'action'].startswith('lobby_'):
            action = message[u'action'][6:] #remove 'lobby_' from string

            {
                'session_logon': self.logon_bcast,
                'session_logout': self.logout_bcast,
                'chat': self.chat_received,
            }[action](message)
        elif message[u'action'] == u'ping':
            #TODO would respond with pong, but handler is missing in server
            pass

    def logon_bcast(self, message):
        user = message[u'username']
        self.add_user(user)
        self.signal_ui(ui_messages.logon(user))
        logging.info('User {0} logs in'.format(user))

    def logout_bcast(self, message):
        user = message[u'username']
        self.remove_user(user)
        self.signal_ui(ui_messages.logout(user))
        logging.info('User logs out'.format(user))

    def lobby_parse(self, message):
        if message[u'action'] == u'lobby_info':
            newrooms = [r for r in message[u'rooms'] if r not in self.rooms]
            self.rooms.append(newrooms)
            self.update_users(message[u'users'])
        elif message[u'action'] == u'lobby_session_logon':
            #FIXME should use logon_bcast(), right?
            self.signal_ui(ui_messages.logon(message[u'username']))
            self.signal_ui(ui_messages.enable_chat())

        self.read_handler = self.common_parse

    def chat_received(self, message):
        sender = message[u'sender']
        text = message[u'message']

        self.signal_ui(ui_messages.chat_received(sender, text))

    def chat_send(self, text):
        message = { u'action': 'lobby_chat', u'message': text }
        self.write(self.message_handler.to_string(message))

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
