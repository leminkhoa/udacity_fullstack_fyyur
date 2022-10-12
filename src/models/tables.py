from app_config import db
from src.models.enums import GenresEnum, StateEnum
from sqlalchemy import TypeDecorator, cast
from sqlalchemy.dialects.postgresql import ARRAY
import re

class ArrayOfEnum(TypeDecorator):
    impl = ARRAY
    cache_ok = True

    def bind_expression(self, bindvalue):
        return cast(bindvalue, self)

    def result_processor(self, dialect, coltype):
        super_rp = super(ArrayOfEnum, self).result_processor(
            dialect, coltype)
        pattern = re.compile(r"^{(.*)}$")

        def handle_raw_string(value):
            inner = pattern.match(value).group(1)
            return _split_enum_values(inner)


        def process(value):
            if value is None:
                return None
            return super_rp(handle_raw_string(value))
        return process


def _split_enum_values(array_string):
    '''https://gerrit.sqlalchemy.org/c/sqlalchemy/sqlalchemy/+/3369/7/lib/sqlalchemy/dialects/postgresql/array.py#370'''
    if '"' not in array_string:
        # no escape char is present so it can just split on the comma
        return array_string.split(",")

    # handles quoted strings from:
    # r'abc,"quoted","also\\\\quoted", "quoted, comma", "esc \" quot", qpr'
    # returns
    # ['abc', 'quoted', 'also\\quoted', 'quoted, comma', 'esc " quot', 'qpr']
    text = array_string.replace(r"\"", "_$ESC_QUOTE$_")
    text = text.replace(r"\\", "\\")
    result = []
    on_quotes = re.split(r'(")', text)
    in_quotes = False
    for tok in on_quotes:
        if tok == '"':
            in_quotes = not in_quotes
        elif in_quotes:
            result.append(tok.replace("_$ESC_QUOTE$_", '"'))
        else:
            result.extend(re.findall(r"([^\s,]+),?", tok))
    return result


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.Enum(StateEnum))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(ArrayOfEnum(db.Enum(GenresEnum)))
    facebook_link = db.Column(db.String(120), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.Enum(StateEnum))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres =  db.Column(ArrayOfEnum(db.Enum(GenresEnum)))
    facebook_link = db.Column(db.String(120), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True)

class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.String(120), primary_key=True)
    venue_id = db.Column(db.String(120), db.ForeignKey('venue.id'))
    artist_id = db.Column(db.String(120), db.ForeignKey('artist.id'))
    start_time = db.Column(db.Time())


db.create_all()