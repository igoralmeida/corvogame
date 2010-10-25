import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../rules')

from mock_session import MockSession
from war import wargame
import random
import war

def test_session_sorted_lands():
    random.seed(10)
    sessions = []
    game = wargame.Wargame()
    
    map(lambda x: sessions.append(MockSession('session' + str(x))), xrange(5))
    map(lambda x: game.register_session(x), sessions)
    
    game.sort_lands(game.LANDS, sessions)

    for s1, s2 in [ (a,b) for a in sessions for b in sessions if a != b ]:
        repeated_lands = [ land for land in s1['land_data'] if land in s2['land_data'] ]
        assert not repeated_lands
    
    sorted_lands = sum([ len(x['land_data']) for x in sessions])      
    assert sorted_lands == len(game.LANDS)
    
    game.stop()
    game.join()

def test_not_present_colors():
    game = wargame.Wargame()
    
    player_mock =  [ { 'self_color' : 'red' } , { 'self_color' : 'blue' } ]
    
    objectives = game.OBJECTIVES
    game.remove_not_present_colors(player_mock, objectives)
    
    assert not 'Defeat the White army.' in objectives and not 'Defeat the Black army.' in objectives

    game.stop()
    game.join()

def test_sorted_objectives():
    random.seed(10)
    sessions = []
    game = wargame.Wargame()     
    
    map(lambda x: sessions.append(MockSession('session' + str(x))), xrange(5))
    map(lambda x: game.register_session(x), sessions)
    
    for player, color in zip(sessions, war.COLORS):
        player['self_color'] = color
            
    game.sort_objectives(game.OBJECTIVES, sessions)
    
    def asserter(session):
        assert 'objective' in session
        assert 'objective_checker' in session
        
    map ( asserter , sessions )
    
    game.stop()
    game.join()

def start_game():
    random.seed(10)
        
    sessions = []
    game = wargame.Wargame()     
    
    map(lambda x: sessions.append(MockSession('session' + str(x))), xrange(5))
    map(lambda x: game.register_session(x), sessions)
    
    game.start_game()
    
    def assert_initial_data(session):
        assert session.expect('wargame_handshake')
        assert session.expect('wargame_startup_info')
        
    map(lambda x: assert_initial_data(x), sessions)
    
    game.stop()
    game.join()

def test_get_continents():
    game = wargame.Wargame()
    
    mock = { 'land_data' : dict(map(lambda land: (land, 0) , game.CONTINENTS['South America'])) }
    
    continents = game.get_continents(mock)
    
    assert 'South America' in continents

    mock['land_data'].update(dict(map(lambda land: (land, 0) , game.CONTINENTS['North America'])))
    
    continents = game.get_continents(mock)
    
    assert 'South America' and 'North America' in continents

    game.stop()
    game.join()
    
def test_get_player_turn_pieces():
    game = wargame.Wargame()

    mock = { 'land_data' : dict(map(lambda land: (land, 0) , game.CONTINENTS['South America'])) }
    
    pieces = game.get_player_turn_pieces(mock)
    
    assert pieces == 7
    
    game.stop()
    game.join()
