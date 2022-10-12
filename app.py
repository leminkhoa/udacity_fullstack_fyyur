#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import collections
import collections.abc
import json
import logging
from flask import render_template, request, Response, flash, redirect, url_for
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from src.models.tables import *
from src.utils import generate_uuid, format_datetime
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app_config import app, moment, csrf, db, migrate
collections.Callable = collections.abc.Callable


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
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
  return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  response = dict(
    count = len(venues),
    data = [dict(id=venue.id, name=venue.name, num_upcoming_shows=len(venue.shows)) for venue in venues]
  )
  return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<venue_id>')
def show_venue(venue_id):
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
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate():
    try:
      venue = Venue(
        id = generate_uuid(),
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        address = form.address.data,
        phone = form.phone.data,
        image_link = form.image_link.data,
        genres = form.genres.data,
        facebook_link = form.facebook_link.data,
        website_link = form.website_link.data,
        seeking_talent = form.seeking_talent.data,
        seeking_description = form.seeking_description.data,
      )
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + form.name.data + ' was successfully listed!')
    except Exception as err:
      db.session.rollback()
      flash('Venue ' + form.name.data + ' Could not be listed!')
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(f"'{field}' : {err[0]}")
    flash('Errors: ' + '  |  '.join(message))
    return render_template('forms/new_venue.html', form=form)
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  artists = db.session.query(Artist).all()
  for artist in artists:
    record = dict(
      id = artist.id,
      name = artist.name,
    )
    data.append(record)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  response = dict(
    count = len(artists),
    data = [dict(id=artist.id, name=artist.name, num_upcoming_shows=len(artist.shows)) for artist in artists]
  )
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<artist_id>')
def show_artist(artist_id):
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
      venue_name = show.venue.name,
      venue_image_link = show.venue.image_link,
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
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist_info = Artist.query.filter(Artist.id==artist_id).first()
  artist_info.genres = map(lambda genres: genres._value_, artist_info.genres)
  artist_info.state = artist_info.state._value_
  form = ArtistForm(obj=artist_info)
  artist = dict(
    id = artist_info.id,
    name = artist_info.name,
    genres = artist_info.genres,
    city = artist_info.city,
    state = artist_info.state,
    phone = artist_info.phone,
    website = artist_info.website_link,
    facebook_link = artist_info.facebook_link,
    seeking_venue = artist_info.seeking_venue,
    seeking_description = artist_info.seeking_description,
    image_link = artist_info.image_link,
  )
  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.get(artist_id)
  try:
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.image_link = request.form['image_link']
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    artist.website_link = request.form['website_link']
    artist.seeking_venue = True if 'seeking_venue' in request.form.keys() else False 
    artist.seeking_description = request.form['seeking_description']
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except Exception as err:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue_info = Venue.query.filter(Venue.id==venue_id).first()
  venue_info.genres = map(lambda genres: genres._value_, venue_info.genres)
  venue_info.state = venue_info.state._value_
  form = VenueForm(obj=venue_info)
  venue = dict(
    id = venue_info.id,
    name = venue_info.name,
    genres = venue_info.genres,
    city = venue_info.city,
    state = venue_info.state,
    address = venue_info.address,
    phone = venue_info.phone,
    website = venue_info.website_link,
    facebook_link = venue_info.facebook_link,
    seeking_talent = venue_info.seeking_talent,
    seeking_description = venue_info.seeking_description,
    image_link = venue_info.image_link,
  )
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get(venue_id)
  try:
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']
    venue.website_link = request.form['website_link']
    venue.seeking_talent = True if 'seeking_talent' in request.form.keys() else False 
    venue.seeking_description = request.form['seeking_description']
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except Exception as err:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  if form.validate():
    try:
      artist = Artist(
          id = generate_uuid(),
          name = form.name.data,
          city = form.city.data,
          state = form.state.data,
          phone = form.phone.data,
          image_link = form.image_link.data,
          genres = form.genres.data,
          facebook_link = form.facebook_link.data,
          website_link = form.website_link.data,
          seeking_venue = form.seeking_venue.data,
          seeking_description = form.seeking_description.data,
      )
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + form.name.data + ' was successfully listed!')
    except Exception as err:
      db.session.rollback()
      flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(f"'{field}' : {err[0]}")
    flash('Errors: ' + '  |  '.join(message))
    return render_template('forms/new_artist.html', form=form)
  return render_template('pages/home.html')

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  if form.validate():
    try:
      show = Show(
          id = generate_uuid(),
          venue_id = form.venue_id.data,
          artist_id = form.artist_id.data,
          start_time = form.start_time.data,
      )
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    except IntegrityError as e:
      db.session.rollback()
      flash('Integrity Error occurred. Please make sure entered IDs are valid IDs')

    except Exception as err:
      db.session.rollback()
      flash(Exception)
      flash('An error occurred. Show could not be listed.')
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(f"'{field}' : {err[0]}")
    flash('Errors: ' + '  |  '.join(message))
    return render_template('forms/new_show.html', form=form)
  return render_template('pages/home.html')

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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
