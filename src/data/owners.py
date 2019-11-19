import mongoengine
import datetime


class Owner(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    name = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)

    snake_ids = mongoengine.ListField()  # list of snakes and cages he owns, the ids
    cage_ids = mongoengine.ListField()

    meta = {
        'db_alias': 'core',  # goes to core database can go to any
        'collection': 'owners'  # this doc belongs ot owner collection
    }
