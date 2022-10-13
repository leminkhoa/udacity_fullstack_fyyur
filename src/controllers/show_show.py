import sys
from app_config import app, db
from flask import request, render_template, abort
from src.models.tables import Show
from datetime import datetime
from forms import *
from src.utils import generate_uuid, format_datetime
from sqlalchemy.exc import IntegrityError


@app.route('/shows')
def shows():
  error500 = False
  data = []
  try:
    shows = db.session.query(Show).all()
    for show in shows:
      # Skip if venue_id or artist_id is missed
      if show.venue is None or show.artist is None:
        continue
      record = dict(
        venue_id = show.venue_id,
        venue_name = show.venue.name,
        artist_id = show.artist_id,
        artist_name = show.artist.name,
        artist_image_link = show.artist.image_link,
        start_time = str(show.start_time),
      )
      data.append(record)
  except Exception:
    error500 = True
    print(sys.exc_info())
  if error500:
    abort (500)
  return render_template('pages/shows.html', shows=data)
