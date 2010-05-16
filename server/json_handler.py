# -*- coding: utf-8 -*-
import json

class Handler(object):
  def from_string(self, raw_message):
    ''' Basic reader. Searches for endlines, strip unused character's and tries to parse them as json objects '''
    assert type(raw_message) == str
    output = []
    errors = []
    if raw_message.rfind("\n") >= 0:
      messages = raw_message.strip().split('\n')
      
      for message in messages:
	try:
	  msg = json.loads(message)
	  output.append(msg)
	except Exception, e:
	  print e
	  errors.append({ "error" : "Malformed input" })    

    return (True, output, errors)
    
  def to_string(self, message):
    try:     
      return json.dumps(message)
    except e:
      print e
      