from app_config import app, db
from flask import render_template, request, Response, flash, redirect, url_for, jsonify
from src.models.tables import Venue
from forms import *


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
