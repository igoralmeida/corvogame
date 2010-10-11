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
import logging

def validate_message(message, session, required_fields):
  req = [ f for f in required_fields if f not in message ]
  if req:
    logging.debug("Missing required fields: {0}".format(req))
    session.write({ 'action' : 'message_reject' , 'error' : 'missing required fields: ' + ' '.join(req) })
    return False
  return True

def validate_field_values(message, session, field, value, values):
  if not value in values:
    session.write({ 'action' : 'message_reject' , 'error' : 'invalid value [{0}] for field [{1}]'.format(value, field) } )
    return False
  return True
