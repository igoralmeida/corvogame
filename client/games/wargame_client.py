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

import abstract_game

import logging

class WargameHandler(abstract_game.GameHandler):
    available_colors = []
    available_capabilities = []

    def __init__(self):
        abstract_game.GameHandler.__init__(self)
        self.read_handler = self.lobby_handler

    def lobby_handler(self, msg):
        logging.debug('Wargame handling message {0}'.format(msg))

        action = msg[u'action'][14:] #remove 'wargame_lobby_' from msg

        if action == 'game_capabilities':
            colors = msg[u'available_colors']
            self.update_colors(colors)

            caps = msg[u'capabilities']
            self.update_capabilities(caps)
        elif action == 'join':
            pass

    def update_colors(self, colors):
        self.available_colors = colors

    def update_capabilities(self, caps):
        self.available_capabilities = caps

