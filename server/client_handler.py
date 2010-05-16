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

class ClientHandler(asyncore.dispatcher):
    """ Basic low level handler. Implents write capabilities, as well as some
    other useful methods
    """

    # TODO: thread/tasklets for buffer incoming handling as passing all data on
    # the same socket thread can be hazardous

    def __init__(self, conn):
        asyncore.dispatcher.__init__(self, conn)
        self.obuffer = []

    def write(self, data):
        self.obuffer.append(data)

    def shutdown(self):
        self.obuffer.append(None)

    def writable(self):
        return self.obuffer

    def handle_write(self):
        if self.obuffer[0] is None:
            self.close()
            return

        sent = self.send(self.obuffer[0])
        if sent >= len(self.obuffer[0]):
            self.obuffer.pop(0)
        else:
            self.obuffer[0] = (self.obuffer[0])[sent:]

