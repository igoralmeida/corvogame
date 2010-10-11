# -*- coding: utf-8 -*-
#    This file is part of corvogame.
#
#    corvogame is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    corvogame is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with corvogame.  If not, see <http://www.gnu.org/licenses/>.

NAME = 'wargame'
DESCRIPTION = '''Wargame - A strategy game'''    
ADDITIONAL_INFO = {}
MAX_PLAYERS = 6
AUTHOR= 'Victor Vicente de Carvalho'
VERSION= '0.0.1'

from wargame_lobby import WargameLobby

def build_lobby(**kwargs):
  return WargameLobby(**kwargs)
