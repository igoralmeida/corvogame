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


import asyncore
import threading
import logging

from common import json_handler
import client_connection
import config
#from gui_ui import PyQt4Graphical_Ui as ui
from cli_ui import Cli_Ui as ui

logging.basicConfig(level=logging.DEBUG, format= '%(asctime)s %(levelname)-8s %(module)-20s[%(lineno)-3d] %(message)s')

if __name__ == "__main__":
    logging.debug("Starting corvogame...") 
    interface = ui()
    interface.start()
    asyncore_thread = threading.Thread(target=asyncore.loop)

    cfg = config.Config()
    client = client_connection.Client(config=cfg, ui=interface)
    client.register_message_handler("json", json_handler.Handler())

    try:
        logging.info("Corvogame is running...")
        asyncore_thread.start()
        interface.blocking_loop()
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Closing corvogame client")
        logging.debug("Stopping client")
        client.shutdown()
        asyncore_thread.join(.5)
        logging.debug("done")

        logging.debug("Joining UI")
        interface.stop()
        interface.join(.5)
        logging.debug("done")
        logging.info("Shutdown complete.")

