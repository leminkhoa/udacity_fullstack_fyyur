from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Regexp, URL, Length, ValidationError
from src.models.enums import GenresEnum, StateEnum
# from src.utils.validators import my_length_check

genres_choices = GenresEnum.__members__.keys()
state_choices = StateEnum.__members__.keys()

def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)

    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)

    return _length

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name',
        validators=[DataRequired(), Length(max=120)]
    )
    city = StringField(
        'city',
        validators=[DataRequired(), Length(max=120)]
    )
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=state_choices
    )
    address = StringField(
        'address',
        validators=[DataRequired(), Length(max=120)]
    )
    phone = StringField(
        'phone',
        validators=[Regexp(r'\d{3}-\d{3}-\d{4}',
                    message='Please enter a proper phone number')]
    )
    image_link = StringField(
        'image_link',
        validators=[URL(), Length(max=120)]
    )
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=genres_choices
    )
    facebook_link = StringField(
        'facebook_link',
        validators=[URL(), Length(max=120)]
    )
    website_link = StringField(
        'website_link',
        validators=[URL(), Length(max=120)]
    )
    seeking_talent = BooleanField(
        'seeking_talent'
    )
    seeking_description = StringField(
        'seeking_description'
    )


class ArtistForm(Form):
    name = StringField(
        'name',
        validators=[DataRequired(), Length(max=120)]
    )
    city = StringField(
        'city',
        validators=[DataRequired(), Length(max=120)]
    )
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=state_choices
    )
    phone = StringField(
        'phone',
        validators=[Regexp(r'\d{3}-\d{3}-\d{4}',
                    message='Please enter a proper phone number')]
    )
    image_link = StringField(
        'image_link',
        validators=[URL(), Length(max=120)]
    )
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=genres_choices
    )
    facebook_link = StringField(
        'facebook_link',
        validators=[URL(), Length(max=120)]
    )
    website_link = StringField(
        'website_link',
        validators=[URL(), Length(max=120)]
    )
    seeking_venue = BooleanField(
        'seeking_venue'
    )
    seeking_description = StringField(
        'seeking_description'
    )
