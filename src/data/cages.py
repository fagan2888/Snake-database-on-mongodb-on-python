import mongoengine
import datetime
from data.bookings import Booking

class Cage(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    price = mongoengine.FloatField(required=True)
    square_meters = mongoengine.FloatField(required=True)
    name = mongoengine.StringField(required=True)
    is_carpeted = mongoengine.BooleanField(required = True)
    allow_dangerous_snakes = mongoengine.BooleanField( default = False)
    has_toys = mongoengine.BooleanField(required=True)

    bookings = mongoengine.EmbeddedDocumentListField(Booking)
    meta = {
        'db_alias' :'core', #goes to core database can go to any
        'collection': 'cages'#this doc belongs ot cages collection
    }