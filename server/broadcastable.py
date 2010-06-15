# -*- coding: utf-8 -*-
import threading
import Queue
import logging

class Broadcastable(threading.Thread):
    def __init__(self):
        logging.debug("Initializing broadcastable")
        threading.Thread.__init__(self)
        self.to_broadcast = []
        self.message_queue = Queue.Queue()
        self.is_alive = True

    def add_to_broadcast(self, item):
        self.to_broadcast.append(item)

    def remove_from_broadcast(self, item):
        if item in self.to_broadcast:
            self.to_broadcast.append(item)

    def stop(self):
        self.is_alive = False
        self.message_queue.put(None)

    def broadcast(self, from_item, message):
        logging.debug("Broadcasting message {0}".format(message))
        self.message_queue.put(message)
        logging.debug("done on broadcasting")

    def run(self):
        logging.debug("Initializing broadcast thread")
        while self.is_alive:
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
