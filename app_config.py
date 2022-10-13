#----------------------------------------------------------------------------#
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from src.utils import format_datetime

# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
csrf = CSRFProtect(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.jinja_env.filters['datetime'] = format_datetime
