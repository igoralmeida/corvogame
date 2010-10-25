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
from common import broadcastable
import random
import logging
from threading import Timer
import logging
import math
import copy

class Wargame(broadcastable.Broadcastable):
    TURN_TIMER = 30
    
    LANDS = [
      'Alaska' ,
      'Mackenzie' ,
      'Vancouver' ,
      'Ottawa' ,
      'Labrador' ,
      'California' ,
      'New York' ,
      'Groeland' , 
      'Mexico' ,
      'Colombia' ,
      'Peru' ,
      'Brasil' ,
      'Argentina' ,
      'Island' ,
      'Germany' ,
      'Sweden' ,
      'Moscow' ,
      'Poland' ,
      'England' ,
      'France' ,
      'Niger' ,
      'Egypt'  ,
      'Sudan' ,
      'Congo' ,
      'South Africa' ,
      'Madagascar' ,
      'Middle Orient' ,
      'Aral' ,
      'Omsk' ,
      'India' ,
      'Vietna' ,
      'China' ,
      'Mongolia' ,
      'Tchita',
      'Siberia' ,
      'Vladvostok'  ,
      'Japan' ,
      'Dudinka',
      'Sumatra' ,
      'Borneo' ,
      'New Guine' ,
      'Australia'
    ]
    
    LAND_LIMIT = {
      'Alaska' : ['Mackenzie','Vancouver','Vladvostok'],
      'Mackenzie' : ['Groeland','Ottawa','Vancouver','Alaska'],
      'Vancouver' : ['Alaska','Mackenzie','Ottawa','California'],
      'Ottawa' : ['Mackenzie','Vancouver','Labrador','New York'],
      'California' : ['Vancouver','New York','Mexico'],
      'Labrador' : ['Groeland','Ottawa','New York'],
      'New York' : ['Ottawa','Labrador','California'],
      'Brasil' : ['Peru','Colombia','Argentina','Congo'],
      'Groeland' : ['Labrador','Mackenzie'],
      'Mexico' : ['California','New York','Colombia'],
      'Colombia' : ['Mexico','Peru','Brasil'],
      'Peru' : ['Colombia','Argentina','Brasil'],
      'Argentina' : ['Peru','Brasil'],
      'Island' : ['Groeland','England','Sweden'],
      'England' : ['Sweden','Germany','France','Island'],
      'France' : ['Germany','Poland','England','Niger','Egypt'],
      'Poland' : ['Germany','France','Moscow'],
      'Sweden' : ['England','Moscow','Island','Germany'],
      'Germany' : ['France','Poland','Sweden','England'],
      'Moscow' : ['Omsk','Aral','Middle Orient','Poland','Sweden'],
      'Niger' : ['Niger','Brasil','Egypt','Sudan','Congo','France'],
      'Egypt' : ['Niger','France','Poland','Sudan','Middle Orient'],
      'Sudan' : ['Madagascar','South Africa','Congo','Egypt','Niger'],
      'Madagascar' : ['Sudan','South Africa'],
      'South Africa' : ['Congo' , 'Sudan','Madagascar'],
      'Congo' : ['Niger','Sudan','South Africa'],
      'Middle Orient' : ['Poland','Aral','Egypt'],
      'India' : ['Sumatra','China','Vietna','Aral','Middle Orient'],
      'Vietna' : ['Borneo','China','India'],
      'China' : ['Aral','Omsk','Mongolia','Vladvostok','Tchita','India','Vietna','Japan'],
      'Aral' : ['Moscow','Middle Orient','India','China','Omsk'],
      'Omsk' : ['Moscow','Aral','China','Mongolia','Dudinka'],
      'Dudinka' : ['Omsk','Mongolia','Tchita','Siberia'],
      'Siberia' : ['Dudinka','Tchita','Vladvostok'],
      'Vladvostok' : ['Alaska','Japan','China','Tchita','Siberia'],
      'Tchita' : ['Siberia','Vladvostok','Mongolia','Dudinka','China'],
      'Japan' : ['Vladvostok','China'] 
    }
 
    CONTINENTS = {
      'South America' : ['Brasil','Colombia','Peru','Argentina'],
      'North America' : ['Alaska' ,'Mackenzie','Vancouver','Ottawa','Labrador','California','New York','Groeland','Mexico'],
      'Africa' : ['Niger','Egypt','Sudan','Congo','South Africa','Madagascar'],
      'Europe' : ['Island','Germany','Sweden','Moscow','Poland','England','France'],
      'Asia' : ['Middle Orient','Aral','Omsk','India','Vietna','China','Mongolia','Tchita','Siberia','Vladvostok','Japan','Dudinka'],
      'Oceania' : [ 'Sumatra','Borneo','New Guine','Australia']
    }
    
    OBJECTIVES = [
      'Defeat the Red army.',
      'Defeat the White army.',
      'Defeat the Blue army.',
      'Defeat the Black army.' ,
      'Defeat the Green army.',
      'Defeat the Yellow army.',
      'Conquest Asia and South America in totallity.',
      'Conquest 18 territories and ocupy every one of them with at least 2 troops.',
      'Conquest North America and Oceania in totallity.',
      'Conquest Europe, Oceania and one more continent at your choice.',
      'Conquest North America and Africa in totallity.',
      'Conquest Asia and Africa in totallity.',
      'Conquest 24 territories at your choice.',  
      'Conquest in totallity Europe, South America and one more continent at your choice.'
    ]
    
    COLOR_TO_OBJECTIVE_INDEX = {
        'red' : 0,
        'white' : 1,
        'blue' : 2,
        'black' : 3,
        'green' : 4,
        'yellow' : 5 
    }
    
    OBJECTIVE_TO_COLOR = {
        'Defeat the Red army.' : 'red',
        'Defeat the White army.' : 'white',
        'Defeat the Blue army.' : 'blue',
        'Defeat the Black army.' : 'black',
        'Defeat the Green army.' : 'green',
        'Defeat the Yellow army.' : 'yellow'    
    }
    
    PIECES_PER_CONTINENT = {
      'South America' : 4,
      'North America' : 5,
      'Africa' : 4,
      'Europe' : 5,
      'Asia' : 7,
      'Oceania' : 2
    }
    
    def check_defeated(self, color):
        for player in self.playing_sessions:
            if player['self_color'] == color and not len(player['land_data']):
                return True
        return False      
    
    #Defeat the Red army
    def check_objective_0(self, player):
        return self.check_defeated('red')
                        
    #Defeat the White army
    def check_objective_1(self, player):
        return self.check_defeated('white')
    
    #Defeat the Blue army
    def check_objective_2(self, player):
        return self.check_defeated('blue')
    
    #Defeat the Black Army
    def check_objective_3(self, player):
        return self.check_defeated('black')

    #Defeat the Green army        
    def check_objective_4(self, player):
        return self.check_defeated('green')

    #Defeat the Yellow army
    def check_objective_5(self, player):
        return self.check_defeated('yellow')
    
    #Conquest Asia and South America in totallity.
    def check_objective_6(self, player):
        return 'Asia' and 'South America' in self.get_continents(player)
    
    #Conquest 18 territories and ocupy every one of them with at least 2 troops.
    def check_objective_7(self, player):
        return len(player['land_data']) >= 18 and reduce(lambda x,y : x['count'] + y['count'], player['land_data']) >= 36 

    #Conquest North America and Oceania in totallity.
    def check_objective_8(self, player):
        return 'North America' and 'Oceania' in self.get_continents(player)
    
    #Conquest Europe, Oceania and one more continent at your choice.
    def check_objective_9(self, player):
        continents = self.get_continents(player)
        return 'Europe' and 'Oceania' in continents and len(continents) >= 3
    
    #Conquest North America and Africa in totallity.
    def check_objective_10(self, player):
        return 'North America' and 'Africa' in self.get_continents(player)
        
    #Conquest Asia and Africa in totallity.
    def check_objective_11(self, player):
        return 'Asia' and 'Africa' in self.get_continents(player)
    
    #Conquest 24 territories at your choice.
    def check_objective_12(self, player):
        return len(player['land_data']) >= 24
        
    #Conquest in totallity Europe, South America and one more continent at your choice.
    def check_objective_13(self, player):
        continents = self.get_continents(player)
        return 'Europe' and 'South America' in continents and len(continents) >= 3
        
    def get_continents(self, player):
        #iters over continents, and for each one filter the lands that are NOT in player data
        #this is to make the size of the sublist as small as possible
        return [ continent for continent in self.CONTINENTS
                     if not filter (lambda continent_land: continent_land not in player['land_data'], self.CONTINENTS[continent]) ]
    
    def get_player_turn_pieces(self, player):
        #get the default pieces and add the bonuses per continent
        pieces = int(math.floor(len(player['land_data']) / 2))
        if pieces < 3: pieces = 3
        pieces += sum([self.PIECES_PER_CONTINENT[continent] for continent in self.get_continents(player)])
        
        return pieces
    
    def __init__(self):
        broadcastable.Broadcastable.__init__(self)

        self.playing_sessions = []
        self.handlers = { 'wargame_add_piece' : self.handle_wargame_add_piece,
                          'wargame_remove_piece' : self.handle_wargame_remove_piece, 
                          'wargame_attack_land' :  self.handle_wargame_attack_land,
                          'wargame_chat': self.handle_wargame_chat,
                          'wargame_end_turn': self.handle_wargame_end_turn  }

        self.validations = { 'wargame_add_piece'   : [ 'to',  'quantity'],
                                    'wargame_remove_piece': [ 'from','quantity'],
                                    'wargame_attack_land' : [ 'to' , 'from' , 'quantity' ],
                                    'wargame_chat'        : [ 'message' ] }

        self.player_deadline_timer = None
        self.turn_total_time = 0

        self.start()

    def handle_wargame_end_turn(self, session, message):
        if not self.validate_is_player_turn(session):
            return
            
        if session['objective_checker'](session):
            #player won the game
            self.broadcast({'action' : 'wargame_game_update', 'text' : 'player {0} won the game!'.format(session.username) })
            self.broadcast({'action' : 'wargame_game_update_status', 'status' : 'shutdown' , 'reason' : 'game has ended' })            
            return

    def handle_wargame_chat(self, session, message):
        logging.debug("Handling chat message for session {0}".format(message))
        message["sender"] = session.username
        self.broadcast(session, message)
    
    def validate_is_player_turn(self, session):
        logging.debug('Validating valid turn for session {0}'.format(session))
        if not self.playing_sessions[self.active_player] == session:
            session.write({'action' : 'wargame_forbidden_action', 'reason' : 'not your turn' })
            return False
        
        return True
    
    def handle_wargame_add_piece(self, session, message):
        logging.debug('Handling piece add for session {0}'.format(session))
        if not self.validate_is_player_turn(session):
            return

        to_land = message['to']

        if from_land not in session['land_data']:
            session.write({ 'action' : message['action'] , 'status' : 'reject', 'reason' : 'not land owner' })
            return

    def handle_wargame_remove_piece(self, session, message):
        pass

    def handle_wargame_attack_land(self, session, message):
        logging.debug('Handling land attack request from session {0}'.format(session))
        if not self.validate_is_player_turn(session):
            return

        from_land = message['from']
        to_land = message['to']

        if from_land not in session['land_data']:
            session.write({ 'action' : message['action'] , 'status' : 'reject', 'reason' : 'not land owner' })
            return

        if to_land in session['land_data']:
            session.write({ 'action' : message['action'] , 'status' : 'reject', 'reason' : 'trying to atack a land owned by you' })
            return        

    #/brief: sort lands and players, and calculate lands that are over the minimum
    def sort_lands(self, lands, players):
        minimum_lands = len(lands) / len(players)
        sorted_lands = random.sample(lands, len(lands))

        #sorting sampled lands between players
        i = 0
        for player in players:
            player['land_data'] = {}
            
            def assign_land(land): 
                player['land_data'][land] = { 'count' : 0 }
                
            map(lambda land: assign_land(land), sorted_lands[i : i + minimum_lands])
            i += minimum_lands
     
        sorted_players = random.sample(players, len(players))

        #add remaining lands to a sorted player list
        for player, land in zip(sorted_players, sorted_lands[i:]):    
            player['land_data'][land] = { 'count' : 0 }
            player['over_landed'] = True

    #removing objectives for where a player color is not present
    #ugly code, improve this!
    def remove_not_present_colors(self, players, objectives):
        mapped_objectives = ['red', 'white', 'blue', 'black', 'green', 'yellow']        
        player_colors = [player['self_color'] for player in players]
        
        not_present_objectives = map(lambda item: self.OBJECTIVES[mapped_objectives.index(item)] , 
                                        filter(lambda color: color not in player_colors, mapped_objectives))

        map(lambda item: objectives.remove(item), not_present_objectives)
        
    def sort_objectives(self, objectives, players):
        objectives = copy.copy(objectives)
 
        self.remove_not_present_colors(players, objectives)

        def re_sort():
            return random.sample(objectives, len(players))
        
        sorted_objectives = re_sort()
        while filter(lambda zipped: zipped[0]['self_color'] == self.OBJECTIVE_TO_COLOR[zipped[1]], zip(players, sorted_objectives)):
            sorted_objectives = re_sort() 
        
        for player, objective in zip(players, sorted_objectives):
            player['objective'] = objective
            player['objective_checker'] = getattr(self, 'check_objective_{0}'.format(self.OBJECTIVES.index(objective)))

    def sort_player_order(self, players):
        players = random.sample(players, len(players))

    def set_player_data(self, players):
        for player in players:
            player['remaining_pieces'] = self.get_player_turn_pieces(player)
    
    def start_game(self):
        logging.debug('Starting a wargame game')
        self.sort_lands(self.LANDS, self.playing_sessions)
        self.sort_objectives(self.OBJECTIVES, self.playing_sessions)
        self.sort_player_order(self.playing_sessions)
        self.set_player_data(self.playing_sessions)
        
        for player in self.playing_sessions:
            self.send_handshake(player)
            player.write({ 'action' : 'wargame_startup_info' , 
                           'owned_land_data' : player['land_data'], 
                           'objective' : player['objective'] })

        self.active_player = -1
        self.notify_turn_change()

        self.player_deadline_timer = Timer(0, self.handle_turn_timer_update)
        self.player_deadline_timer.start()
        
    def handle_session_disconnect(self, session):
        logging.debug("Handling session disconnect for session {0}".format(session.username))

        self.remove_from_broadcast(session)
        self.playing_sessions.remove(session)
        #TODO: What to do here? end the game?
        
        msg = { u'action' : 'wargame_session_logout', u'username' : session.username , u'user_id' : session.user_id }
        self.broadcast({u'session' : 'lobby'} , msg)
            
    def notify_turn_change(self):
        logging.debug('Updating turn')
        self.active_player += 1
        player = self.playing_sessions[self.active_player % len(self.playing_sessions)]
        
        player['remaining_pieces'] = self.get_player_turn_pieces(player)
        
        self.broadcast(None, { 'action' : 'wargame_status_update_turn', 
                               'player' : player.username,
                               'remaining_pieces' : player['remaining_pieces'] } )

        self.turn_total_time = 0                               
        self.player_deadline_timer = Timer(5, self.handle_turn_timer_update)   
        self.player_deadline_timer.start()                                   
    
    def handle_turn_timer_update(self):
        logging.debug('Updating turn timer.')
        def timer_tick():
            self.player_deadline_timer = Timer(5, self.handle_turn_timer_update)   
            self.player_deadline_timer.start()         

        if self.turn_total_time >= self.TURN_TIMER:
            self.notify_turn_change()

            return

        self.turn_total_time += 5        
        self.playing_sessions[self.active_player % len(self.playing_sessions)].write({'action' : 'wargame_turn_tick',
                                                                                      'time' : self.turn_total_time })
        timer_tick()
        
    def stop(self):
        if self.player_deadline_timer:
            self.player_deadline_timer.cancel()
    
        broadcastable.Broadcastable.stop(self)
    
    def send_handshake(self, session):
        logging.debug('sending handshake to {0}'.format(session))
        session.write({'action' : 'wargame_handshake', 'message' : 'welcome to wargame!'})
    
    def register_session(self, session):
        logging.debug('registering session {0}'.format(session))
       
        session.incoming_message_handler = self.on_session_message
        session.close_handler = self.handle_session_disconnect
        
        session.inject_validators(self.validations)
        
        self.playing_sessions.append(session)
        self.add_to_broadcast(session)
        
    def on_session_message(self, session, message):
        logging.debug("Received message {0} from user {1}".format(message, session.username))
        if message["action"] in self.handlers:
            self.handlers[message["action"]](session, message)    
      
