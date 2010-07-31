# -*- coding: utf-8 -*-

NAME = 'wargame'
DESCRIPTION = '''Wargame - A strategy game'''    
ADDITIONAL_INFO = {}
MAX_PLAYERS = 6
AUTHOR= 'Victor Vicente de Carvalho'
VERSION= '0.0.1'

from wargame import Wargame

def build_game(**kwargs):
    return Wargame(kwargs)
