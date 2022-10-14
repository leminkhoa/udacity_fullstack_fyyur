from app_config import app, db
from flask import render_template, request, flash, redirect, url_for, jsonify
from src.models.tables import Artist
from forms import *


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
