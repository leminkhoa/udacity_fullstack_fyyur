import sys
from app_config import app, db
from flask import flash, request, render_template
from src.models.tables import Show
from forms import *
from src.utils import generate_uuid
from sqlalchemy.exc import IntegrityError


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
      print(sys.exc_info())
      db.session.rollback()
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
