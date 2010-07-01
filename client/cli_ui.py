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

import ui
import logging
import readline
import threading

class Cli_Ui(ui.Common_Ui, threading.Thread):
    ''' Command-line user interface. '''

    def __init__(self):
        ui.Common_Ui.__init__(self)
        threading.Thread.__init__(self)
        self.is_alive = True

    def user_logon(self, user):
        print '{0} entrou'.format(user)

    def user_logout(self, user):
        print '{0} saiu'.format(user)

    def chat_send(self, text):
        if self.conhandler is not None:
            self.conhandler.chat_send(text)

    def prompt(self):
        return 'c> '

    def stop(self):
        self.is_alive = False

    def run(self):
        logging.debug("Initializing ui thread")

        while self.is_alive:
            _in = raw_input(self.prompt())
            self.chat_send(_in)

