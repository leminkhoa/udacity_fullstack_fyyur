import sys
from app_config import app, db
from flask import request, render_template, abort
from src.models.tables import Venue
from datetime import datetime


@app.route('/venues')
def venues():
  error500 = False
  try:
    # Get distinct regions (city + state)
    regions = db.session.query(
      Venue.city,
      Venue.state
      )\
      .distinct()\
      .all()
    # For each region, append venue records
    data = []
    for (city, state) in regions:
      venues = db.session.query(Venue.id, Venue.name)\
          .filter(Venue.city==city, Venue.state==state.value)\
          .all()
      record = dict(
        city = city,
        state = state.value,
        venues = [dict(id=venue[0], name=venue[1], num_upcoming_shows=1) for venue in venues],
      )
      data.append(record)
  except Exception:
    error500 = True
    print(sys.exc_info())
  if error500:
    abort (500)  
  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  error500 = False
  try:
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    response = dict(
      count = len(venues),
      data = [dict(id=venue.id, name=venue.name, num_upcoming_shows=len(venue.shows)) for venue in venues]
    )
  except Exception:
    error500 = True
    print(sys.exc_info())
  if error500:
    abort (500)

  return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<venue_id>')
def show_venue(venue_id):
  error404 = False
  error500 = False
  try:
    venue_info = db.session.query(
      Venue.id, 
      Venue.name,
      Venue.genres,
      Venue.address,
      Venue.city,
      Venue.state,
      Venue.phone,
      Venue.website_link,
      Venue.facebook_link,
      Venue.seeking_talent,
      Venue.seeking_description,
      Venue.image_link
    )\
    .filter(Venue.id==venue_id)\
    .first()
  
    # Find shows by venue_id
    upcoming_shows = []
    past_shows = []
    list = Venue.query.get(venue_id)
    for show in list.shows:
      show_rec = dict(
        artist_id = show.artist_id,
        artist_name = show.artist.name,
        artist_image_link = show.artist.image_link,
        start_time = str(show.start_time)
      )
      if show.start_time < datetime.now():
        past_shows.append(show_rec)
      else:
        upcoming_shows.append(show_rec)

    
      data = dict(
        id  = venue_info[0],
        name  = venue_info[1],
        genres = [genre._value_ for genre in venue_info[2]],
        address = venue_info[3],
        city = venue_info[4],
        state = venue_info[5]._value_,
        phone = venue_info[6],
        website = venue_info[7],
        facebook_link = venue_info[8],
        seeking_talent = venue_info[9],
        seeking_description = venue_info[10],
        image_link = venue_info[11],
        upcoming_shows = upcoming_shows,
        past_shows = past_shows,
        past_shows_count = len(past_shows),
        upcoming_shows_count = len(upcoming_shows),
      )
  except AttributeError:
    error404 = True
    print(sys.exc_info())
  except Exception:
    error500 = True
    print(sys.exc_info())
  if error404:
    abort (404)
  if error500:
    abort (500)
  return render_template('pages/show_venue.html', venue=data)
