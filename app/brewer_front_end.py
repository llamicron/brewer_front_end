from flask import Flask, render_template, request, redirect
from peewee import *
from models.recipe import Recipe
import json
import os

db_path = os.path.expanduser("~") + "/.brewer.db"

app = Flask(__name__)
db = SqliteDatabase(db_path)


@app.before_request
def _db_connect():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


def form_missing_field(form):
    for field, value in form.iteritems():
        if value == "":
            return True
    return False


# Routes

@app.route("/")
def index():
    recipes = Recipe.select()
    return render_template("index.html", recipes=recipes)


@app.route("/create-recipe", methods=['POST'])
def hand_create_recipe_post():
    if form_missing_field(request.form):
        # Set error message
        return redirect("/")
    # Store recipe
    recipe = Recipe.create(
        name=request.form['name'],
        grain=request.form['grain'],
        grain_temp = request.form['grain_temp'],
        water = request.form['water'],
        mash_temp = request.form['mash_temp'],
        mash_time = request.form['mash_time'],
        description = request.form['description']
    )
    recipe.save()
    return redirect("/")


if __name__ == '__main__':
    Recipe.create_table(True)
    app.run(extra_files="static/main.js")
