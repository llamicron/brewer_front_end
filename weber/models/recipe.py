from peewee import *
from settings import db_file

db = SqliteDatabase(db_file)

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
