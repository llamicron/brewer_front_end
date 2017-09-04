from peewee import *
from .. import settings

db = SqliteDatabase(settings.db_file)

class Recipe(Model):
    name        = CharField()
    grain       = FloatField()
    grain_temp  = FloatField()
    water       = FloatField()
    mash_temp   = FloatField()
    mash_time   = FloatField()
    description = CharField()

    class Meta:
        database = db
