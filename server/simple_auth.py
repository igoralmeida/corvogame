# -*- coding: utf-8 -*-

def authenticate(msg):
  return msg[u'username'] == 'user' and msg[u'password'] == '123456'