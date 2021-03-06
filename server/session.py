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

from common.client_handler import ClientHandler
import logging
import uuid
import threading
import time

class Session(ClientHandler):
    def __init__(self, unknown_connection):
        self.username = unknown_connection.username
        ClientHandler.__init__(self, unknown_connection.socket)
        self.obuffer = self.obuffer + unknown_connection.obuffer
        self.message_handler = unknown_connection.message_handler
        self.read_handler = self.handle_session_messages
        self.incoming_message_handler = None
        self.user_id = uuid.uuid1().get_hex()
        self.close_handler = None
        self.data_holder = {}
        self.message_validators =  {}
        
    def inject_validators(self, actions):
        self.message_validators.update(actions)
        
    def remove_validators(self, actions):
        for action in actions:
            del self.message_validators[action]

    def __setitem__(self, key, value):
        self.data_holder[key] = value
    
    def __getitem__(self, key):
        if key in self.data_holder:
          return self.data_holder[key]
        raise StopIteration
        
    def __contains__(self, item):
        return item in self.data_holder
        
    def ping(self):
        #self.write({'action' : 'ping', 'time' : str(time.time()) })
        self.write({'action' : 'ping' })

    def handle_session_messages(self, message):
        logging.debug("Received message {0} from session user {1}".format(message, self.username))
        
        if not 'action' in message:
            self.write({'action' : 'message_reject', 'reason' : 'missing "action" tag'})
            return
            
        if message['action'] in self.message_validators:
            not_present = [ field for field in self.message_validators[message['action']] if not field in message ]
            if not_present:
                self.write({'action' : 'message_reject', 'action' : message['action'],  'reason' : 'missing required fields: {0}'.format(not_present) })             
                return
                
        if self.incoming_message_handler:
            logging.debug("Sending to handler {0}".format(self.incoming_message_handler))
            self.incoming_message_handler(self, message)

    def shutdown(self):
        logging.debug("shutdown, close handler is {0}".format(self.close_handler))

        if self.close_handler:
            self.close_handler(self)

        ClientHandler.shutdown(self)

        self.message_handler = None
        self.read_handler = None
        self.incoming_message_handler = None
        self.close_handler = None

    def write(self, message):
        logging.debug("Writting message {0} to user {1}".format(message, self.username))
        ClientHandler.write(self, self.message_handler.to_string(message))
