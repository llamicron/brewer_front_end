from peewee import *
from settings import db_file

db = SqliteDatabase(db_file)

class Procedure(Model):
    name = CharField()


    class Meta:
        database = db
