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

import threading
import Queue
import logging

class Broadcastable(threading.Thread):
    def __init__(self):
        logging.debug("Initializing broadcastable")
        threading.Thread.__init__(self)
        self.to_broadcast = []
        self.message_queue = Queue.Queue()
        self.running = True
        
    def add_to_broadcast(self, item):
        self.to_broadcast.append(item)

    def remove_from_broadcast(self, item):
        if item in self.to_broadcast:
            self.to_broadcast.remove(item)

    def stop(self):
        self.running = False
        self.message_queue.put(None)

    def broadcast(self, from_item, message):
        logging.debug("Broadcasting message {0}".format(message))
        self.message_queue.put(message)
        logging.debug("done on broadcasting")

    def run(self):
        logging.debug("Initializing broadcast thread")
        while self.running:
            try:
                try:
                    message = self.message_queue.get()

                    if not self.is_alive:
                        continue

                    logging.debug("Broadcasting message: {0}".format(message))

                    for item in self.to_broadcast:
                        logging.debug("Writting on item {0}".format(item))
                        item.write(message)
                finally:
                    self.message_queue.task_done()

            except Exception,e:
                logging.error("Error on lobby broadcast thread: {0}".format(e))
