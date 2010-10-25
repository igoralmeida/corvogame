import sys
sys.path.append('..')
sys.path.append('rules')

import war.wargame_lobby as lobby
import uuid
import war
from mock_session import MockSession
    
class MockLobby(object):
  pass

def test_setting_color():
  room_owner = MockSession('room_owner')
  l = lobby.WargameLobby(MockLobby(),room_owner, {'room_name' : 'cocada' }, uuid.uuid1().get_hex())
  
  assert(l.available_colors == war.COLORS)
  
  session1 = MockSession('user1')
  l.add_session(session1, {})
  
  assert(session1['self_color'] not in l.available_colors)
  
  l.handle_set_self_color(session1, { 'action' : 'lobby_set_self_color', 'color' : 'red'} )
  session1.expect('wargame_lobby_player_updated_color')
  assert('red' not in session1.expect('wargame_lobby_available_colors')['colors'])
  
  l.stop()
  l.join()

def test_setting_same_color():
  room_owner = MockSession('room_owner')
  l = lobby.WargameLobby(MockLobby(),room_owner, {'room_name' : 'cocada' }, uuid.uuid1().get_hex())
  
  assert(l.available_colors == war.COLORS)
  
  session1 = MockSession('user1')
  l.add_session(session1, {})
  
  assert(session1['self_color'] not in l.available_colors)
  
  l.handle_set_self_color(session1, { 'action' : 'wargame_lobby_set_self_color', 'color' : 'red'} )
  session1.expect('wargame_lobby_player_updated_color')
  
  assert('red' not in session1.expect('wargame_lobby_available_colors')['colors'])
  
  session1.purge()  
  l.handle_set_self_color(session1, { 'action' : 'wargame_lobby_set_self_color', 'color' : 'red'} )
  
  assert(session1.expect('wargame_lobby_set_self_color')['status'] == 'error')
  
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
  
  l.handle_set_self_color(session1, { 'action' : 'wargame_lobby_set_self_color', 'color' : 'red'} )
  print session2.expect('wargame_lobby_player_updated_color')
  assert(session2.expect('wargame_lobby_player_updated_color')['username'] == session1.username)
  session1.purge()
    
  l.handle_set_self_color(session2, { 'action' : 'wargame_lobby_set_self_color', 'color' : 'blue'} )
  print session1.expect('wargame_lobby_player_updated_color')
  
  equal_users = session1.expect('wargame_lobby_player_updated_color')['username'] == session2.username
  print session1.expect('wargame_lobby_player_updated_color')['username']
  assert(equal_users)
  
  l.stop()
  l.join()

def test_change_color():
  room_owner = MockSession('room_owner')  
  l = lobby.WargameLobby(MockLobby(),room_owner, {'room_name' : 'cocada' }, uuid.uuid1().get_hex())
  
  session1 = MockSession('user1')
  l.add_session(session1, {})
  
  l.handle_set_self_color(session1, { 'action' : 'wargame_lobby_set_self_color', 'color' : 'red'} )
  session1.expect('wargame_lobby_player_updated_color')
  session1.purge()
  
  l.handle_set_self_color(session1, { 'action' : 'wargame_lobby_set_self_color', 'color' : 'red'} )
  
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
  
  session1.expect('wargame_lobby_player_ready_state')
  session2.expect('wargame_lobby_player_ready_state')
  session3.expect('wargame_lobby_player_ready_state')
  
  l.handle_start_game(session1, { } )  
  
  print "waiting for session1 lobby start game rejection due not having ownership"
  
  assert( session1.expect( 'wargame_lobby_start_game' )['status'] == 'error' )
  assert( session1.expect( 'wargame_lobby_start_game' )['reason'] == 'you are not the room owner' )
  
  print "done"
  
  l.handle_start_game(room_owner, { } )
  
  print "waiting for room owner lobby start game rejection due not all players being ready"
  
  assert( room_owner.expect( 'wargame_lobby_start_game' )['status'] == 'error' )
  assert( room_owner.expect( 'wargame_lobby_start_game' )['reason'] == 'there are players not ready to play' )
 
  print "done"
  
  l.handle_set_self_ready(session4, { 'ready' : 'true' } )
  l.handle_start_game(room_owner, { 'action' : 'wargame_lobby_start_game' } )
  
  l.stop()
  l.join()
