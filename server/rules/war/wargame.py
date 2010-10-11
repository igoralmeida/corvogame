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
import broadcastable
import random
import logging

class Wargame(broadcastable.Broadcastable):
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

    def __init__(self):
      self.playing_sessions = []
    
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
      def add_player(player,land):
        player['lands'].append(land)
        player['over_landed'] = True
        
      map(add_player, sorted_players, sorted_lands[i:])
      
    def start(self):
      self.sort_lands(self.LANDS, self.playing_sessions)
      self.sort_objectives()
    
    def stop(self):
      broadcastable.Broadcastable.stop(self)
    
    def send_handshake(self, session):
      session.send({'action' : 'game_handshake', 'message' : 'welcome to wargame!'})
    
    def register_session(self, session):
      self.playing_sessions.append(session)
      self.send_handshake(session)
