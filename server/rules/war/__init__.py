# -*- coding: utf-8 -*-

NAME = 'wargame'
DESCRIPTION = '''Wargame - A strategy game'''    
ADDITIONAL_INFO = {}
MAX_PLAYERS = 6
AUTHOR= 'Victor Vicente de Carvalho'
VERSION= '0.0.1'

from lobby import WargameLobby

def build_lobby(**kwargs):
  return WargameLobby(**kwargs)
