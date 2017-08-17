from peewee import *
import settings

db = SqliteDatabase(settings.db_file)

class Procedure(Model):
    name = CharField()


    class Meta:
        database = db
