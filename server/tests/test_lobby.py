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
import sys
sys.path.append('..')
sys.path.append('rules')

import war.wargame_lobby as lobby
import uuid
import logging
import time
import py

class MockSession (object):
  def __init__(self, username):
    self.received_messages = {}
    self.username = username
    self.data_holder = {}
    
  def __setitem__(self, key, value):
    #print 'setitem {0} {1}'.format(key, value)
    self.data_holder[key] = value
  
  def __getitem__(self, key):
    #print 'getitem {0}'.format(key)
    
    if key in self.data_holder:
      return self.data_holder[key]
      
    raise StopIteration
  
  def __contains__(self, item):
    return item in self.data_holder
  
  def expect(self, action):
    for i in xrange(10):
      if action not in self.received_messages.keys():
        time.sleep(0.1)
      else:
        return self.received_messages[action]
    
    raise Exception(action)
    
  def purge(self):
    self.received_messages = {}
  
  def write(self, message):
    self.received_messages[message['action']] =  message
    
  def __str__(self):
    return 'MockSession [{0}]'.format(self.username)
    
class MockLobby(object):
  pass

def test_setting_color():
  room_owner = MockSession('room_owner')
  l = lobby.WargameLobby(MockLobby(),room_owner, {'room_name' : 'cocada' }, uuid.uuid1().get_hex())
  
  assert(l.available_colors == l.COLORS)
  
  session1 = MockSession('user1')
  l.add_session(session1, {})
  
  assert(session1['self_color'] not in l.available_colors)
  
  l.handle_set_self_color(session1, { 'action' : 'lobby_set_self_color', 'color' : 'red'} )
  session1.expect('game_lobby_player_updated_color')
  assert('red' not in session1.expect('game_lobby_available_colors')['colors'])
  
  l.stop()
  l.join()


def test_setting_same_color():
  room_owner = MockSession('room_owner')
  l = lobby.WargameLobby(MockLobby(),room_owner, {'room_name' : 'cocada' }, uuid.uuid1().get_hex())
  
  assert(l.available_colors == l.COLORS)
  
  session1 = MockSession('user1')
  l.add_session(session1, {})
  
  assert(session1['self_color'] not in l.available_colors)
  
  l.handle_set_self_color(session1, { 'action' : 'game_lobby_set_self_color', 'color' : 'red'} )
  session1.expect('game_lobby_player_updated_color')
  
  assert('red' not in session1.expect('game_lobby_available_colors')['colors'])
  
  session1.purge()  
  l.handle_set_self_color(session1, { 'action' : 'game_lobby_set_self_color', 'color' : 'red'} )
  
  assert(session1.expect('game_lobby_set_self_color')['status'] == 'error')
  
  l.stop()
  l.join()

def test_setting_color_users():
  room_owner = MockSession('room_owner')
  l = lobby.WargameLobby(MockLobby(),room_owner, {'room_name' : 'cocada' }, uuid.uuid1().get_hex())
  
  session1 = MockSession('user1')
  session2 = MockSession('user2')
  
  l.add_session(session1, {})
  l.add_session(session2, {})
  
  assert(session1['self_color'] not in l.available_colors)
  assert(session2['self_color'] not in l.available_colors)
  
  l.handle_set_self_color(session1, { 'action' : 'game_lobby_set_self_color', 'color' : 'red'} )
  print session2.expect('game_lobby_player_updated_color')
  assert(session2.expect('game_lobby_player_updated_color')['username'] == session1.username)
  
  l.handle_set_self_color(session2, { 'action' : 'game_lobby_set_self_color', 'color' : 'blue'} )
  print session1.expect('game_lobby_player_updated_color')
  assert(session1.expect('game_lobby_player_updated_color')['username'] == session2.username)
  
  l.stop()
  l.join()

def test_change_color():
  room_owner = MockSession('room_owner')  
  l = lobby.WargameLobby(MockLobby(),room_owner, {'room_name' : 'cocada' }, uuid.uuid1().get_hex())
  
  session1 = MockSession('user1')
  l.add_session(session1, {})
  
  l.handle_set_self_color(session1, { 'action' : 'game_lobby_set_self_color', 'color' : 'red'} )
  session1.expect('game_lobby_player_updated_color')
  session1.purge()
  
  l.handle_set_self_color(session1, { 'action' : 'game_lobby_set_self_color', 'color' : 'red'} )
  
  print session1
  
  l.stop()
  l.join()

def test_ready_game():
  room_owner = MockSession('room_owner')  
  l = lobby.WargameLobby(MockLobby(),room_owner, {'room_name' : 'cocada' }, uuid.uuid1().get_hex())

  session1 = MockSession('user1')
  session2 = MockSession('user2')
  session3 = MockSession('user3')
  session4 = MockSession('user4')
  
  l.add_session(session1, {})
  l.add_session(session2, {})
  l.add_session(session3, {})
  l.add_session(session4, {})
  
  l.handle_set_self_ready(session1, { 'ready' : 'true' } )
  l.handle_set_self_ready(session2, { 'ready' : 'true' } )
  l.handle_set_self_ready(session3, { 'ready' : 'true' } )
  
  session1.expect('game_lobby_player_ready_state')
  session2.expect('game_lobby_player_ready_state')
  session3.expect('game_lobby_player_ready_state')
  
  l.handle_start_game(session1, { } )  
  
  print "waiting for session1 lobby start game rejection due not having ownership"
  
  assert( session1.expect( 'game_lobby_start_game' )['status'] == 'error' )
  assert( session1.expect( 'game_lobby_start_game' )['reason'] == 'you are not the room owner' )
  
  print "done"
  
  l.handle_start_game(room_owner, { } )
  
  print "waiting for room owner lobby start game rejection due not all players being ready"
  
  assert( room_owner.expect( 'game_lobby_start_game' )['status'] == 'error' )
  assert( room_owner.expect( 'game_lobby_start_game' )['reason'] == 'there are players not ready to play' )
 
  print "done"
  
  l.handle_set_self_ready(session4, { 'ready' : 'true' } )
  l.handle_start_game(room_owner, { 'action' : 'game_lobby_start_game' } )
  
  l.stop()
  l.join()
