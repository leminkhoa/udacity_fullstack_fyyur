import sys
from app_config import app, db
from flask import flash, request, render_template
from src.models.tables import Artist
from forms import *
from src.utils import generate_uuid


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
    except Exception:
      print(sys.exc_info())
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
