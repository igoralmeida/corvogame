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
    
    #Defeat the Red army
    def check_objective_0(self, player):
        pass
        
    #Defeat the White army
    def check_objective_1(self, player):
        pass
    
    #Defeat the Blue army
    def check_objective_2(self, player):
        pass
    
    #Defeat the Black Army
    def check_objective_3(self, player):
        pass    

    #Defeat the Green army        
    def check_objective_4(self, player):
        pass

    #Defeat the Yellow army
    def check_objective_5(self, player):
        pass
    
    def check_objective_6(self, player):
        pass
        
    def check_objective_7(self, player):
        pass

    def check_objective_8(self, player):
        pass
        
    def check_objective_9(self, player):
        pass
        
    def check_objective_10(self, player):
        pass
        
    def check_objective_11(self, player):
        pass
        
    def check_objective_12(self, player):
        pass
        
    def check_objective_13(self, player):
        pass

    def __init__(self):
        self.playing_sessions = []
        self.handlers = { 'wargame_add_piece' : self.handle_wargame_add_piece,
                          'wargame_remove_piece' : self.handle_wargame_remove_piece, 
                          'wargame_attack_land' :  self.handle_wargame_attack_land,
                          'wargame_chat': self.handle_wargame_chat  }

        self.validations = { 'wargame_add_piece'   : [ 'to',  'quantity'],
                                    'wargame_remove_piece': [ 'from','quantity'],
                                    'wargame_attack_land' : [ 'to' , 'from' , 'quantity' ],
                                    'wargame_chat'        : [ 'message' ] }
                                    
        self.turn_deadline_timer = None
        self.turn_total_time = 0
    
    def handle_wargame_chat(self, session, message):
        logging.debug("Handling chat message")
        message["sender"] = session.username
        self.broadcast(session, message)
    
    def handle_wargame_add_piece(self, session, message):
        pass
    
    def handle_wargame_remove_piece(self, session, message):
        pass
     
    def handle_wargame_attack_land(self, session, message):
        pass
    
    #/brief: sort lands and players, and calculate lands that are over the minimum
    def sort_lands(self, lands, players):
        minimum_lands = len(lands) / len(players)
        sorted_lands = random.sample(lands, len(lands))

        #sorting sampled lands between players
        i = 0
        for player in players:
            player['lands'] = sorted_lands[i : i + minimum_lands]
            i += minimum_lands
            
        sorted_players = random.sample(players, len(players))

        #add remaining lands to a sorted player list
        for player, land in zip(sorted_players, sorted_lands[i:]):    
            player['lands'].append(land)
            player['over_landed'] = True
      
    def sort_objectives(self, objectives, players):
        sorted_objectives = random.sample(objectives, len(players))
        
        for player, objective in zip(players, sorted_objectives):
            player['objective'] = objective
            player['objective_checker'] = getattr(self, 'check_objective_{0}'.format(self.OBJECTIVES.index(objective)))
    
    def sort_player_order(self, players):
        players = random.sample(players, len(players))
        
    def start(self):
        self.sort_lands(self.LANDS, self.playing_sessions)
        self.sort_objectives(self.OBJECTIVES, self.playing_sessions)
        self.sort_player_order(self.playing_sessions)

        self.active_player = -1        
        self.notify_turn_change()

        self.player_deadline_timer = threading.Timer(1, self.handle_turn_timer_update)
        
    def handle_session_disconnect(self, session):
        logging.debug("Handling session disconnect for session {0}".format(session.username))

        self.remove_from_broadcast(session)

        if session.username in self.sessions:
            del self.sessions[session.username]

        #TODO: What to do here? end the game?
        
        msg = { u'action' : 'wargame_session_logout', u'username' : session.username , u'user_id' : session.user_id }
        self.broadcast({u'session' : 'lobby'} , msg)
            
    def notify_turn_change(self):
        self.active_player += 1
        
        self.broadcast(None, { 'action' : 'wargame_status_update_turn', 
                               'player' : self.playing_sessions[self.active_player % len(self.playing_sessions)].username } )
    
    def handle_turn_timer_update(self):
        if self.turn_total_time >= self.TURN_TIMER:
            self.notify_turn_change()
            return

        self.player_deadline_timer = threading.Timer(1, self.handle_turn_timer_update)
        self.turn_total_time += 1
        
        self.playing_sessions[self.active_player % len(self.playing_sessions)].write({'action' : 'wargame_turn_tick',
                                                                                      'time' : self.turn_total_time,
                                                                                      'remaining' : self.TURN_TIMER - self.turn_total_time })
        
    def stop(self):
        broadcastable.Broadcastable.stop(self)
    
    def send_handshake(self, session):
        session.write({'action' : 'game_handshake', 'message' : 'welcome to wargame!'})
    
    def register_session(self, session):
        session.incoming_message_handler = self.on_session_message
        session.close_handler = self.handle_session_disconnect
        
        session.inject_validators(self.validations)
        
        self.playing_sessions.append(session)
        self.send_handshake(session)
      
    def on_session_message(self, session, message):
        logging.debug("Received message {0} from user {1}".format(message, session.username))
        if message["action"] in self.handlers:
            self.handlers[message["action"]](session, message)    
      
