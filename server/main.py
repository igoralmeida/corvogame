# -*- coding: utf-8 -*-

import server_listener
import simple_auth
import json_handler
import lobby
import asyncore

_lobby = lobby.Lobby()

def add_to_lobby(session):
  _lobby.handshake(session)
  
  
if __name__ == "__main__":
  server = server_listener.ServerListener("0.0.0.0", 5000)
  
  server.register_auth_handler(simple_auth.authenticate)
  server.register_message_handler("json", json_handler.Handler() )
  server.register_logon_handler(add_to_lobby)
    
  try:
    asyncore.loop(timeout=4.0)
  except KeyboardInterrupt:
    print "Closing corvogame server"
    server.shutdown()
    print "done"