from peewee import *
import os

db = SqliteDatabase(os.path.expanduser("~") + "/.brewer.db")

class Recipe(Model):
    name       = CharField()
    grain      = FloatField()
    grain_temp = FloatField()
    water      = FloatField()
    mash_temp  = FloatField()
    mash_time  = FloatField()

    class Meta:
        database = db
