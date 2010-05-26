#!/usr/bin/python
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

from common import json_handler
import asyncore
import logging
import client_connection

logging.basicConfig(level=logging.DEBUG, format= '%(asctime)s %(levelname)-8s %(module)-20s[%(lineno)-3d] %(message)s')

if __name__ == "__main__":
    logging.debug("Starting corvogame...")
    client = client_connection.Client()

    client.register_message_handler("json", json_handler.Handler())

    try:
        logging.info("Corvogame is running...")
        asyncore.loop(timeout=1.0)
    except KeyboardInterrupt:
        logging.info("Closing corvogame client")
        logging.debug("Stopping client")
        client.shutdown()
        logging.debug("done")
        logging.info("Shutdown complete.")

