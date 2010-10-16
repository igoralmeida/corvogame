import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../rules')

from mock_session import MockSession
from war import wargame
import random

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

def test_sorted_objectives():
    random.seed(10)
    sessions = []
    game = wargame.Wargame()     
    
    map(lambda x: sessions.append(MockSession('session' + str(x))), xrange(5))
    map(lambda x: game.register_session(x), sessions)
    
    game.sort_objectives(game.OBJECTIVES, sessions)
    
    def asserter(session):
        assert 'objective' in session
        assert 'objective_checker' in session
        
    map ( asserter , sessions )

def test_simple_game():
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
    
    
    
    
        
