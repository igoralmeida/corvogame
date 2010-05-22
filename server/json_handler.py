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

import json
import logging

class Handler(object):
    def from_string(self, raw_message):
        ''' Basic reader. Searches for endlines, strip unused character's and tries to parse them as json objects '''
        assert type(raw_message) == str
        output = []
        errors = []
        index = 0

        r_index = raw_message.find('\n', index)

        while r_index >= 0:
            logging.debug("Index is {0}, r_index is {1}".format(index, r_index))

            try:
                message = raw_message[index:r_index].rstrip()
                logging.debug("Trying to process: [{0}]".format(message))
                msg = json.loads(message)
                output.append(msg)
            except Exception, e:
                logging.debug("Error processing input: {0}".format(e))
                errors.append({ u"action" : u"error" , u"reason" : u"Malformed input", u'raw_text' : message })

            index = r_index + 1
            r_index = raw_message.find('\n', index)

        logging.debug("raw message length: {0}, index {1}".format(len(raw_message),index))
        return (True, output, errors, raw_message[index:])

    def to_string(self, message):
        logging.debug("Trying to decode input of type {1} : {0}".format(message, type(message)))
        try:
            return json.dumps(message) + "\r\n"
        except e:
            logging.debug("Error processing output: {0}".format(e))
