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

import logging
import threading
from PyQt4 import QtCore, QtGui

import ui
from gui import guiPyQt4

class PyQt4Graphical_Ui(ui.Common_Ui, threading.Thread):
    ''' Graphical user interface using the PyQt4 framework. '''

    def __init__(self):
        ui.Common_Ui.__init__(self)
        threading.Thread.__init__(self)

        self.gui_app = QtGui.QApplication([])
        self.gui_MainWindow = QtGui.QMainWindow()
        self.gui_CorvoGUI = guiPyQt4.Ui_MainWindow()
        self.gui_CorvoGUI.setupUi(self.gui_MainWindow)
        self.gui_MainWindow.show()

        self.is_alive = True

        self.logon_info = None

    def run(self):
        ''' Dummy and useless run() method for threading.Thread.
        This is obsolete because PyQt requires the gui to run on the main event
        thread.
        '''
        logging.debug("Initializing ui thread")

    def blocking_loop(self):
        self.gui_app.exec_()

    def stop(self):
        self.is_alive = False
        self.gui_app.exit()

    def chat_send(self, text):
        if self.conhandler is not None:
            self.conhandler.chat_send(text)

    def chat_received(self, message):
        #FIXME is it a private or a public chat?
        self.generalChat_show('<{0}> {1}\n'.format(message[u'sender'],
            message[u'message']))

    def user_logon_event(self, user):
        ''' Show in the gui someone has logged in '''
        self.generalChat_show('{0} entrou\n'.format(user))

    def user_logout_event(self, user):
        ''' Show in the gui someone has logged out '''
        self.generalChat_show('{0} saiu\n'.format(user))

    def require_logon(self):
        self.store_logon('user 123456')

    def get_logon(self):
        while self.logon_info == None or self.logon_info.__len__() != 2:
            pass

        l, p = self.logon_info
        self.logon_info = None
        return l, p

    def enable_chat(self):
        pass

    def store_logon(self, line):
        parts = line.split()
        if parts.__len__() != 2:
            self.require_logon()
            return

        login, pwd = parts[0], parts[1]
        self.enable_chat()
        self.logon_info = [login, pwd]

    #-----------------
    # PyQt gui helper functions
    #
    # The CamelCase in the first words are only there to differentiate the event
    # from the GUI element.
    #-----------------
    def generalChat_show(self, str):
        self.gui_CorvoGUI.geralChatTabTextBrowser.insertPlainText(str)

    def statusBar_info(self, ui_msg):
        ''' This method centralizes the statusBar handling for the messages in
        ui_messages.py.
        '''

        if ui_msg[u'action'] == u'connection':
            status = ui_msg[u'status']

            if status == u'init':
                str = 'Conectando...'
            elif status == u'established':
                str = 'Conectado!'
            elif status == u'off':
                str = 'Desconectado'

            self.statusBar_show(str)

    def statusBar_show(self, str):
        self.gui_CorvoGUI.statusbar.showMessage(str)

