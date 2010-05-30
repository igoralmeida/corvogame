# -*- coding: utf-8 -*-
from json_handler import Handler
import logging

class WebsocketHandler(Handler):
    NAME = 'json_websocket'
    
    def __init__(self):
        Handler.__init__(self, '0xff')
        
    def from_string(self, raw_message):
        raw_message= raw_message[1:-1]
        Handler.from_string(self, raw_message)
        
    def to_string(self, message):
        encoded_msg = Handler.to_string(self, message)
        return '\x00' + encoded_msg.encode('utf-8') + '\xff'