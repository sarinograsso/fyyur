from datetime import datetime

from sqlalchemy import func

from fyyur import db

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

genres_venues = db.Table('genres_venues',
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True)
)


artists_genres = db.Table('artists_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    genres = db.relationship('Genre', secondary=genres_venues, backref=db.backref('venues', lazy=True))
    shows = db.relationship('Show', backref='venue', lazy='dynamic')

    def past_shows(self):
        return self.shows.filter(Show.start_time < datetime.today()).all()

    def past_shows_count(self):
        return self.shows.filter(Show.start_time < datetime.today()).count()

    def upcoming_shows(self):
        return self.shows.filter(Show.start_time > datetime.today()).all()

    def upcoming_shows_count(self):
        return self.shows.filter(Show.start_time > datetime.today()).count()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'genres': [g.name for g in self.genres],
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description
        }


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    genres = db.relationship('Genre', secondary=artists_genres, backref=db.backref('artists', lazy=True))
    shows = db.relationship('Show', backref='artist', lazy='dynamic')

    def past_shows(self):
        return self.shows.filter(Show.start_time < datetime.today()).all()

    def past_shows_count(self):
        return self.shows.filter(Show.start_time < datetime.today()).count()

    def upcoming_shows(self):
        return self.shows.filter(Show.start_time > datetime.today()).all()

    def upcoming_shows_count(self):
        return self.shows.filter(Show.start_time > datetime.today()).count()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': [g.name for g in self.genres],
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description
        }


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def is_past(self):
        if self.start_time < datetime.today():
            return True
        return False

    def artist_dict(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def venue_dict(self):
        return {
            "venue_id": self.venue_id,
            "venue_name": self.venue.name,
            "venue_image_link": self.venue.image_link,
            "start_time": self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }