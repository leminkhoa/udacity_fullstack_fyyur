import sys
from app_config import app, db
from flask import flash, request, render_template
from src.models.tables import Venue
from forms import *
from src.utils import generate_uuid


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
      print(sys.exc_info())
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