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

class Common_Ui():
    ''' Command-line user interface. '''

    def __init__(self):
        self.conhandler = None

    def register_connection_handler(self, handler):
        self.conhandler = handler

    def chat_send(self, text):
        # TODO raise exception about this being abstract instead
        raise NotImplementedError

    def chat_received(self, message):
        # TODO raise exception about this being abstract instead
        raise NotImplementedError

    def user_logon(self, user):
        raise NotImplementedError

    def user_logout(self, user):
        raise NotImplementedError

