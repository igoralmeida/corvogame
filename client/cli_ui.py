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
import cmd

NOPROMPT = 0
PROMPTING_LOGON = 1
PROMPTING_CHATMSG = 2

class Cli_Ui(ui.Common_Ui, threading.Thread, cmd.Cmd):
    ''' Command-line user interface. '''

    def __init__(self):
        ui.Common_Ui.__init__(self)
        threading.Thread.__init__(self)
        cmd.Cmd.__init__(self)
        self.is_alive = True

        self.state = NOPROMPT
        self.default = None

        self.logon_info = None

    def blocking_loop(self):
        while self.is_alive:
            pass

    def user_logon_event(self, user):
        print '{0} entrou'.format(user)

    def user_logout_event(self, user):
        print '{0} saiu'.format(user)

    def enable_chat(self):
        self.state = PROMPTING_CHATMSG
        self.default = self.handler_chatmsg
        self.prompt = self.chatmsg_prompt()

    def require_logon(self):
        self.state = PROMPTING_LOGON
        self.default = self.handler_logonmsg
        self.prompt = self.logon_prompt()

    def store_logon(self, line):
        parts = line.split()
        if parts.__len__() != 2:
            self.require_logon()
            return

        login, pwd = parts[0], parts[1]
        self.enable_chat()
        self.state = NOPROMPT #don't issue the chat prompt right away
        self.logon_info = [login, pwd]

    def get_logon(self):
        while self.logon_info == None or self.logon_info.__len__() != 2:
            pass

        l, p = self.logon_info
        self.logon_info = None
        return l, p

    def chat_send(self, text):
        if self.conhandler is not None:
            self.conhandler.chat_send(text)

    def logon_prompt(self):
        return 'Senha invalida. Digite login e senha abaixo, separados por espacos\n%> '

    def chatmsg_prompt(self):
        return 'c> '

    def stop(self):
        self.is_alive = False

    def run(self):
        logging.debug("Initializing ui thread")

        while self.is_alive:
            if self.state == NOPROMPT:
                pass
            else:
                self.cmdloop()

    def emptyline(self):
        pass

    def handler_chatmsg(self, str):
        """ This is one of the addresses self.default will point to.
        This handler is responsible for treating the chat message and sending it
        to the conhandler.
        """
        if str.__len__() > 0:
            if str == 'EOF':
                #TODO signal the conhandler and close everything
                pass
            else:
                self.chat_send(str)

    def handler_logonmsg(self, str):
        """ This is one of the addresses self.default will point to.
        This handler is responsible for storing the (possibly correct) logon
        message until the underlying client-handler fetches it with
        self.get_logon()
        """
        self.store_logon(str)

    def do_quit(self, s):
        """ Terminar a GUI e sair """
        self.state = NOPROMPT
        self.stop()
        return True

