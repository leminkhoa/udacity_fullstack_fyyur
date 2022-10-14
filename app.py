#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import collections
import collections.abc
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from src.models.tables import *
from app_config import app, moment, csrf, db, migrate
from src.controllers.index import *
from src.controllers.create_artist import *
from src.controllers.create_venue import *
from src.controllers.create_show import *
from src.controllers.show_artist import *
from src.controllers.show_venue import *
from src.controllers.show_show import *
from src.controllers.delete_venue import *
from src.controllers.update_artist import *
from src.controllers.update_venue import *
from src.error_handler import server_error, not_found_error

collections.Callable = collections.abc.Callable

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
