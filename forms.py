from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Regexp, URL, Length, Optional
from src.models.enums import GenresEnum, StateEnum
from src.validators import facebook_link_validator, start_time_validator

genres_choices = GenresEnum.__members__.keys()
state_choices = StateEnum.__members__.keys()


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired(), start_time_validator],
        format="%Y-%m-%d %H:%M:%S",
        default= datetime.today(),
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
                        message='Please enter a proper phone number'),
                    Length(max=12)]
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
        validators=[Optional(), URL(), facebook_link_validator] 
    )
    website_link = StringField(
        'website_link',
        validators=[Optional(), URL(), Length(max=120)]
    )
    seeking_talent = BooleanField(
        'seeking_talent',
        validators=[Optional()]
    )
    seeking_description = StringField(
        'seeking_description',
        validators=[Optional(), Length(max=120)]
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
                        message='Please enter a proper phone number'),
                    Length(max=12)]
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
        validators=[Optional(), URL(), facebook_link_validator] 
    )
    website_link = StringField(
        'website_link',
        validators=[Optional(), URL(), Length(max=120)]
    )
    seeking_venue = BooleanField(
        'seeking_venue',
        validators=[Optional()]
    )
    seeking_description = StringField(
        'seeking_description',
        validators=[Optional(), Length(max=120)]
    )
