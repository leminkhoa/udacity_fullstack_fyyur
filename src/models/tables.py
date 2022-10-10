from app import db
from src.models.enums import GenresEnum, StateEnum


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.Enum(StateEnum))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.Enum(GenresEnum))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    # shows = db.relationship('VenueShow', backref='venue', lazy=True)


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.Enum(StateEnum))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres =  db.Column(db.Enum(GenresEnum))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    # shows = db.relationship('ArtistShow', backref='artist', lazy=True)

class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.String(120), db.ForeignKey('venue.id'), nullable=True)
    artist_id = db.Column(db.String(120), db.ForeignKey('artist.id'), nullable=True)
    start_time = db.Column(db.Time(timezone=True))


db.create_all()