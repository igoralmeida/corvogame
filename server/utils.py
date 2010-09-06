# -*- coding: utf-8 -*-
import logging

def validate_message(message, session, required_fields):
  req = [ f for f in required_fields if f not in message ]
  if req:
    logging.debug("Missing required fields: {0}".format(req))
    session.write({ 'action' : 'message_reject' , 'error' : 'missing required fields: ' + ' '.join(req) })
    return False
  return True