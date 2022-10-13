#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import collections
import collections.abc
import json
import logging
from flask import render_template, request, Response, flash, redirect, url_for, jsonify
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from src.models.tables import *
from src.utils import generate_uuid, format_datetime
from sqlalchemy.exc import IntegrityError
from datetime import datetime
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
collections.Callable = collections.abc.Callable


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


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
