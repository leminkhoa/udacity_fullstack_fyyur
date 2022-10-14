import sys
from app_config import app, db
from flask import flash, redirect, url_for
from src.models.tables import Venue
from forms import *


@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  try:
    delete_venue = Venue.query.filter(Venue.id==venue_id).first()
    db.session.delete(delete_venue)
    for show in delete_venue.shows:
      print(show)
      # db.session.delete(show)
    db.session.commit()
    flash('Venue ' + delete_venue.name + ' was successfully deleted!')
  except Exception:
    print(sys.exc_info())
    db.session.rollback()
    flash('Venue ' + delete_venue.name + ' Could not be deleted!')
  finally:
    db.session.close()
    return redirect(url_for('venues'))
