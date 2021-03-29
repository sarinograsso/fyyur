from datetime import datetime

from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import desc

from fyyur import app, db
from fyyur.helpers import format_datetime
from fyyur.models import Genre, Venue, Artist, Show
from fyyur.forms import ShowForm, VenueForm, ArtistForm


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def index():
    venues = Venue.query.order_by(desc(Venue.created_at)).limit(10).all()
    artists = Artist.query.order_by(desc(Artist.created_at)).limit(10).all()
    return render_template('pages/home.html', venues=venues, artists=artists)


#  List All Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    data = []
    # Get unique city/state combinations
    areas = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
    # Get all venues for each city/state combination
    for area in areas:
        venues_in_area = Venue.query.filter_by(city=area.city).filter_by(state=area.state).all()
        venue_data = []
        for venue in venues_in_area:
            venue_data.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": venue.upcoming_shows_count()
            })
        data.append({
            "city": area.city,
            "state": area.state,
            "venues": venue_data
        })
    return render_template('pages/venues.html', areas=data)


#  Search Venues
#  ----------------------------------------------------------------


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    search_results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(search_results),
        "data": []
    }
    for venue in search_results:
        response['data'].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": venue.upcoming_shows_count()
        })
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


#  Show Venue
#  ----------------------------------------------------------------


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        return render_template('errors/404.html')

    data = venue.to_dict()

    past_shows = db.session.query(Show).join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()
    past_shows_data = []
    for past_show in past_shows:
        past_shows_data.append(past_show.artist_dict())
    data['past_shows'] = past_shows_data
    data['past_shows_count'] = len(past_shows_data)

    upcoming_shows = db.session.query(Show).join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()
    upcoming_shows_data = []
    for upcoming_show in upcoming_shows:
        upcoming_shows_data.append(upcoming_show.artist_dict())
    data['upcoming_shows'] = upcoming_shows_data
    data['upcoming_shows_count'] = len(upcoming_shows_data)

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.all()]
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    form = VenueForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.all()]
    if form.validate_on_submit():
        try:
            venue = Venue(
              name=request.form['name'],
              city=request.form['city'],
              state=request.form['state'],
              address=request.form['address'],
              phone=request.form['phone'],
              image_link=request.form['image_link'],
              website=request.form['website_link'],
              facebook_link=request.form['facebook_link'],
              seeking_talent= True if 'seeking_talent' in request.form else False,
              seeking_description=request.form['seeking_description']
            )
            venue_genres = Genre.query.filter(Genre.id.in_([int(i) for i in request.form.getlist('genres')])).all()
            venue.genres.extend(venue_genres)
            db.session.add(venue)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        if error:
            flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed, please try again.')
            return render_template('forms/new_venue.html', form=form)
        else:
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
            return redirect(url_for('index'))

    # Errors on form input, render template again showing errors
    return render_template('forms/new_venue.html', form=form)


#  Edit Venue
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        return render_template('errors/404.html')
    form = VenueForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.all()]
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.address.data = venue.address
    form.genres.data = [genre.id for genre in venue.genres]
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website_link.data = venue.website
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False
    venue = Venue.query.get(venue_id)
    form = VenueForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.all()]
    if form.validate_on_submit():
        try:
            venue.name=request.form['name']
            venue.city=request.form['city']
            venue.state=request.form['state']
            venue.address=request.form['address']
            venue.phone=request.form['phone']
            venue.image_link=request.form['image_link']
            venue.website=request.form['website_link']
            venue.facebook_link=request.form['facebook_link']
            venue.seeking_talent= True if 'seeking_talent' in request.form else False
            venue.seeking_description=request.form['seeking_description']
            venue.genres.clear()
            venue_genres = Genre.query.filter(Genre.id.in_([int(i) for i in request.form.getlist('genres')])).all()
            venue.genres.extend(venue_genres)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        if error:
            flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated, please try again.')
            return render_template('forms/edit_venue.html', form=form, venue=venue)
        else:
            flash('Venue ' + request.form['name'] + ' was successfully updated!')
            return redirect(url_for('show_venue', venue_id=venue_id))

    # Errors on form input, render template again showing errors
    return render_template('forms/edit_venue.html', form=form, venue=venue)


#  Delete Venue
#  ----------------------------------------------------------------


@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' + venue.name + ' could not be deleted, please try again.')
        return render_template('pages/show_venue.html', venue=venue)
    else:
        flash('Venue ' + venue.name + ' was successfully deleted!')
        return redirect(url_for('index'))


#  List All Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


#  Search Artists
#  ----------------------------------------------------------------


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    search_results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(search_results),
        "data": []
    }
    for artist in search_results:
        response['data'].append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": artist.upcoming_shows_count()
        })
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


#  Show Artists
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if not artist:
        return render_template('errors/404.html')

    data = artist.to_dict()

    past_shows = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()
    past_shows_data = []
    for past_show in past_shows:
        past_shows_data.append(past_show.venue_dict())
    data['past_shows'] = past_shows_data
    data['past_shows_count'] = len(past_shows_data)

    upcoming_shows = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
    upcoming_shows_data = []
    for upcoming_show in upcoming_shows:
        upcoming_shows_data.append(upcoming_show.venue_dict())
    data['upcoming_shows'] = upcoming_shows_data
    data['upcoming_shows_count'] = len(upcoming_shows_data)

    return render_template('pages/show_artist.html', artist=data)


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.all()]
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    form = ArtistForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.all()]
    if form.validate_on_submit():
        try:
            artist = Artist(
                name=request.form['name'],
                city=request.form['city'],
                state=request.form['state'],
                phone=request.form['phone'],
                image_link=request.form['image_link'],
                website=request.form['website_link'],
                facebook_link=request.form['facebook_link'],
                seeking_venue=True if 'seeking_venue' in request.form else False,
                seeking_description=request.form['seeking_description']
            )
            artist_genres = Genre.query.filter(Genre.id.in_([int(i) for i in request.form.getlist('genres')])).all()
            artist.genres.extend(artist_genres)
            db.session.add(artist)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        if error:
            flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed, please try again.')
            return render_template('forms/new_artist.html', form=form)
        else:
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
            return redirect(url_for('index'))

    # Errors on form input, render template again showing errors
    return render_template('forms/new_artist.html', form=form)


#  Edit Artist
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if not artist:
        return render_template('errors/404.html')
    form = ArtistForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.all()]
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = [genre.id for genre in artist.genres]
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.website_link.data = artist.website
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    artist = Artist.query.get(artist_id)
    form = ArtistForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.all()]
    if form.validate_on_submit():
        try:
            artist.name = request.form['name']
            artist.city = request.form['city']
            artist.state = request.form['state']
            artist.phone = request.form['phone']
            artist.image_link = request.form['image_link']
            artist.website = request.form['website_link']
            artist.facebook_link = request.form['facebook_link']
            artist.seeking_venue = True if 'seeking_venue' in request.form else False
            artist.seeking_description = request.form['seeking_description']
            artist.genres.clear()
            artist_genres = Genre.query.filter(Genre.id.in_([int(i) for i in request.form.getlist('genres')])).all()
            artist.genres.extend(artist_genres)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        if error:
            flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated, please try again.')
            return render_template('forms/edit_artist.html', form=form, artist=artist)
        else:
            flash('Artist ' + request.form['name'] + ' was successfully updated!')
            return redirect(url_for('show_artist', artist_id=artist_id))

    # Errors on form input, render template again showing errors
    return render_template('forms/edit_artist.html', form=form, artist=artist)


#  List All Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    all_shows = Show.query.all()
    for show in all_shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return render_template('pages/shows.html', shows=data)


#  Create Show
#  ----------------------------------------------------------------


@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    form = ShowForm()
    if form.validate_on_submit():
        # check that the provided venue id and artist id exist in DB
        venue = Venue.query.get(request.form['venue_id'])
        artist = Artist.query.get(request.form['artist_id'])
        if venue is None or artist is None:
            flash('Please make sure the Artist ID and the Venue ID exist.')
            return render_template('forms/new_show.html', form=form)
        # both venue and artist exist, can now create the show
        try:
            show = Show(
                artist=artist,
                venue=venue,
                start_time=request.form['start_time']
            )
            db.session.add(show)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        if error:
            flash('An error occurred. The Show could not be listed, please try again.')
            return render_template('forms/new_show.html', form=form)
        else:
            flash('The Show was successfully listed!')
            return redirect(url_for('index'))

    # Errors on form input, render template again showing errors
    return render_template('forms/new_show.html', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

