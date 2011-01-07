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

class GameHandler():
    msg_sender = None
    ui = None

    def __init__(self, msg_sender, ui):
        self.msg_sender = msg_sender
        self.ui = ui

    def lobby_handler(self, msg):
        """ Handles game setup and lobby """
        raise NotImplementedError

    def chat_send(self, text):
        """ Sends chat message to server """
        raise NotImplementedError

    def ui_responder(self, msg):
        """ Centralizes the queries coming from the UI. """
        raise NotImplementedError
