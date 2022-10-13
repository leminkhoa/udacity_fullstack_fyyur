import sys
from app_config import app, db
from flask import request, render_template, abort
from src.models.tables import Artist
from datetime import datetime


@app.route('/artists')
def artists():
  error500 = False
  data = []
  try:
    artists = db.session.query(Artist).all()
    for artist in artists:
      record = dict(
        id = artist.id,
        name = artist.name,
      )
      data.append(record)
  except Exception:
    error500 = True
    print(sys.exc_info())
  if error500:
    abort (500) 
  return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  error404 = False
  error500 = False
  try:
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    response = dict(
      count = len(artists),
      data = [dict(id=artist.id, name=artist.name, num_upcoming_shows=len(artist.shows)) for artist in artists]
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
  return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<artist_id>')
def show_artist(artist_id):
  error404 = False
  error500 = False
  try:
    artist_info = db.session.query(
      Artist.id, 
      Artist.name,
      Artist.genres,
      Artist.city,
      Artist.state,
      Artist.phone,
      Artist.website_link,
      Artist.facebook_link,
      Artist.seeking_venue,
      Artist.seeking_description,
      Artist.image_link
    )\
    .filter(Artist.id==artist_id)\
    .first()
    
    # Find shows by artist_id
    upcoming_shows = []
    past_shows = []
    list = Artist.query.get(artist_id)
    for show in list.shows:
      show_rec = dict(
        venue_id = show.venue_id,
        venue_name = '#' if show.venue is None else show.venue.name,
        venue_image_link = '#' if show.venue is None else show.venue.image_link,
        start_time = str(show.start_time)
      )
      if show.start_time < datetime.now():
        past_shows.append(show_rec)
      else:
        upcoming_shows.append(show_rec)

    
    data = dict(
      id  = artist_info[0],
      name  = artist_info[1],
      genres = [genre._value_ for genre in artist_info[2]],
      city = artist_info[3],
      state = artist_info[4]._value_,
      phone = artist_info[5],
      website = artist_info[6],
      facebook_link = artist_info[7],
      seeking_talent = artist_info[8],
      seeking_description = artist_info[9],
      image_link = artist_info[10],
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
  return render_template('pages/show_artist.html', artist=data)
