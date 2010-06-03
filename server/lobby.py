# -*- coding: utf-8 -*-

import threading
import Queue
import logging

class Lobby(threading.Thread):
    def __init__(self):
        logging.debug("Initializing lobby")
        threading.Thread.__init__(self)

        self.sessions = {}
        self.channels = {}
        self.message_queue = Queue.Queue()

        self.handlers =  { 'chat' : self.handle_chat , 'quit' : self.handle_session_quit }

        self.start()

    def handle_session_quit(session, message):
        logging.debug("Handling session quit")

        del self.sessions[session.username]

        msg = { u'action' : 'session_logout', u'username' : session.username }

        self.broadcast({u'session' : 'lobby'} , msg)

        session.shutdown()

    def handle_chat(self, session, message):
        logging.debug("Handling chat message")
        message["action"] = u'lobby_chat'
        message["sender"] = session.username

        self.broadcast(session, message)

    def get_rooms(self):
        logging.debug("Getting rooms")
        return []

    def get_users(self):
        logging.debug("Getting users")
        users = []

        for username in self.sessions:
            user_msg = {}
            user_msg[u'username'] = username
            users.append(user_msg)

        return users

    def stop(self):
        self.is_alive = False
        self.message_queue.put(None)

    def handshake(self, session):
        logging.debug("Doing handshake for username {0}".format(session.username))
        session.incoming_message_handler = self.on_session_message

        message = {}
        message["action"] = "lobby_info"
        message["rooms"] = self.get_rooms()
        message["users"] = self.get_users()

        session.write(message)

        self.broadcast( { u'session' : 'lobby'} , { u'action' : 'session_logon', u'username' : session.username })
        self.sessions[session.username] = session

    def on_session_message(self, session, message):
        logging.debug("Received message {0} from user {1}".format(message, session.username))
        if message["action"] in self.handlers:
            self.handlers[message["action"]](session, message)


    def broadcast(self, from_session, message):
        logging.debug("Broadcasting message {0} on lobby".format(message))
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
                    for user in self.sessions:
                        logging.debug("Sending to username {0}".format(user))
                        self.sessions[user].write(message)
                finally:
                    self.message_queue.task_done()

            except Exception,e:
                logging.error("Error on lobby broadcast thread: {0}".format(e))
