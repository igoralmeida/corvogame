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

import asyncore
import socket
import logging

class ClientHandler(asyncore.dispatcher):
    ''' Basic low level handler. Implents write capabilities, as some other useful methods

    TODO: thread/tasklets for buffer incoming handling as passing all data on the same socket thread
          can be hazardous
    '''
    def __init__(self, conn=None):
        logging.debug("Initializing ClientHandler")
        asyncore.dispatcher.__init__(self, conn)
        self.message_handler = None
        self.read_handler = None
        self.obuffer = []
        self.inbuffer = ""
        self.error_count = 0

    def write(self, data):
        logging.debug("writting [{0}]".format(data))
        self.obuffer.append(data)

    def shutdown(self):
        logging.debug("shutdown")
        self.obuffer.append(None)

    def writable(self):
        return self.obuffer

    def handle_read(self):
        ''' reads some data and call the current handler '''
        if self.message_handler and self.read_handler:
            print self.read_handler
            data = self.recv(8192)

            logging.debug("Data is {0}".format(len(data)))

            if not data:
                self.shutdown()
                return

            try:
                (status, messages, error, rest) = self.message_handler.from_string(data)
                logging.debug("readed {0} status is {1} error is {3} Rest is [{2}]".format(messages,status,rest,error))
                assert type(messages) == list

                if status == True:
                    for message in messages:
                        logging.debug("Callig read_handler {0} to message: {1}".format(self.read_handler, message))
                        self.read_handler(message)

                    if messages:
                        self.error_count = 0

                    for e in error:
                        logging.debug("Replying parsing error to {0}: {1}".format(self.message_handler, e))
                        self.write(e)
                        self.error_count += len(error)

                    if self.error_count > 5:
                        msg = {}
                        msg["action"] = u'disconnect'
                        msg["reason"] = u'Too many protocol errors'

                        self.write(msg)
                        self.shutdown()

                        return

                    self.inbuffer = rest
                else:
                    self.inbuffer = self.inbuffer + rest
            except:
                self.shutdown()

    def handle_error(self, _type, value, traceback ):
        logging.debug("Tracked an session error of type {0} and value {1}\n Traceback {2}".format(_type, value, traceback))
        self.close()

    def handle_write(self):
        logging.debug("Handle write: {0}".format(self.obuffer))
        if self.obuffer[0] is None:
            self.close()
            return

        sent = self.send(self.obuffer[0])
        if sent >= len(self.obuffer[0]):
            self.obuffer.pop(0)
        else:
            self.obuffer[0] = self.obuffer[0][sent:]
