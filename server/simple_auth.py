# -*- coding: utf-8 -*-

def authenticate(msg):
  ''' a VERY dummy authentication method '''
  return msg[u'username'] == 'user' and msg[u'password'] == '123456'