from app_config import db
from src.models.tables import *

#  Venues
#  ----------------------------------------------------------------


venue_1 = Venue(
    id = "1",
    name = "The Musical Hop",
    genres = ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    address = "1015 Folsom Street",
    city = "San Francisco",
    state = "CA",
    phone = "123-123-1234",
    website_link = "https://www.themusicalhop.com",
    facebook_link = "https://www.facebook.com/TheMusicalHop",
    seeking_talent = True,
    seeking_description = "We are on the lookout for a local artist to play every two weeks. Please call us.",
    image_link = "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
)

venue_2 = Venue(
    id = "2",
    name = "The Dueling Pianos Bar",
    genres = ["Classical", "R&B", "Hip-Hop"],
    address = "335 Delancey Street",
    city = "New York",
    state = "NY",
    phone = "914-003-1132",
    website_link = "https://www.theduelingpianos.com",
    facebook_link = "https://www.facebook.com/theduelingpianos",
    seeking_talent = False,
    image_link = "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
)

venue_3 = Venue(
    id = "3",
    name = "Park Square Live Music & Coffee",
    genres = ["Rock n Roll", "Jazz", "Classical", "Folk"],
    address = "34 Whiskey Moore Ave",
    city = "San Francisco",
    state = "CA",
    phone = "415-000-1234",
    website_link = "https://www.parksquarelivemusicandcoffee.com",
    facebook_link = "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent = False,
    image_link = "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
)

#  Artists
#  ----------------------------------------------------------------

artist_1 = Artist(
    id = "4",
    name = "Guns N Petals",
    genres = ["Rock n Roll"],
    city = "San Francisco",
    state = "CA",
    phone = "326-123-5000",
    website_link = "https://www.gunsnpetalsband.com",
    facebook_link = "https://www.facebook.com/GunsNPetals",
    seeking_venue = True,
    seeking_description = "Looking for shows to perform at in the San Francisco Bay Area!",
    image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
)

artist_2 = Artist(
    id = "5",
    name = "Matt Quevedo",
    genres = ["Jazz"],
    city = "New York",
    state = "NY",
    phone = "300-400-5000",
    facebook_link = "https://www.facebook.com/mattquevedo923251523",
    seeking_venue = False,
    seeking_description = "Looking for shows to perform at in the San Francisco Bay Area!",
    image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
)

artist_3 = Artist(
    id = "6",
    name = "The Wild Sax Band",
    genres = ["Jazz", "Classical"],
    city = "San Francisco",
    state = "CA",
    phone = "432-325-5432",
    seeking_venue = False,
    image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
)

#  Shows
#  ----------------------------------------------------------------

show_1 = Show(
    id = "1",
    venue_id = "1",
    artist_id = "4",
    start_time = "2021-05-21T21:30:00.000Z"
)

show_2 = Show(
    id = "2",
    venue_id = "3",
    artist_id = "5",
    start_time = "2021-06-15T23:00:00.000Z"
)

show_3 = Show(
    id = "3",
    venue_id = "3",
    artist_id = "6",
    start_time = "2021-05-21T21:30:00.000Z"
)

show_4 = Show(
    id = "4",
    venue_id = "3",
    artist_id = "6",
    start_time = "2035-04-08T20:00:00.000Z"
)

show_5 = Show(
    id = "5",
    venue_id = "3",
    artist_id = "6",
    start_time = "2035-04-15T20:00:00.000Z"
)


recs = [venue_1, venue_2, venue_3, artist_1, artist_2, artist_3, show_1, show_2, show_3, show_4, show_5]
db.session.bulk_save_objects(recs)
db.session.commit()
print("Sample records have been successfully added!")
