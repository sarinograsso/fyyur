import re
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField
from wtforms.validators import DataRequired, URL, Regexp, Optional, ValidationError


def validate_phone(self, phone):
    us_phone_num = '^([0-9]{3})[-][0-9]{3}[-][0-9]{4}$'
    match = re.search(us_phone_num, phone.data)
    if not match:
        raise ValidationError('Error, phone number must be in format xxx-xxx-xxxx')


class ShowForm(Form):
    artist_id = IntegerField(
        'artist_id',
        validators=[DataRequired(message="This field is required and must be an integer")]
    )
    venue_id = IntegerField(
        'venue_id',
        validators=[DataRequired(message="This field is required and must be an integer")]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired(message="This field is required and must be YYYY-MM-DD HH:MM:SS")],
        default=datetime.today()
    )


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired(), validate_phone]
    )
    image_link = StringField(
        'image_link', validators=[URL(), Optional()]
    )
    genres = SelectMultipleField(
        'genres',
        choices=[],  # set in the controller from the genres in the DB
        validators=[DataRequired()],
        coerce=int
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Optional()]
    )
    website_link = StringField(
        'website_link', validators=[URL(), Optional()]
    )

    seeking_talent = BooleanField(
        'seeking_talent'
    )

    seeking_description = StringField(
        'seeking_description'
    )


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'phone', validators=[DataRequired(), validate_phone]
    )
    image_link = StringField(
        'image_link', validators=[URL(), Optional()]
    )
    genres = SelectMultipleField(
        'genres',
        choices=[],  # set in the controller from the genres in the DB
        validators=[DataRequired()],
        coerce=int
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Optional()]
    )
    website_link = StringField(
        'website_link', validators=[URL(), Optional()]
    )
    seeking_venue = BooleanField(
        'seeking_venue'
    )
    seeking_description = StringField(
        'seeking_description'
     )

