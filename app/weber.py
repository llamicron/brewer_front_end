from flask import Flask, render_template, request, redirect, url_for, session
from peewee import *
from models.recipe import Recipe
import json
from brewer.controller import Controller
import os

db_path = os.path.expanduser("~") + "/.brewer.db"
con = Controller()

class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    block_start_string='(%',
    block_end_string='%)',
    variable_start_string='((',
    variable_end_string='))',
    comment_start_string='(#',
    comment_end_string='#)',
  ))

app = CustomFlask(__name__)
db = SqliteDatabase(db_path)

app.secret_key = "9aD@nZ6-N9e$NZ[32\oXs4_H42"


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


# Routes ---------------------------------------------------

@app.route("/")
def index():
    recipes = Recipe.select()
    return render_template("index.html", recipes=recipes)

@app.route("/controller")
def controller():
    return render_template("controller.html")


@app.route("/create-recipe", methods=['POST'])
def hand_create_recipe_post():
    if form_missing_field(request.form):
        # TODO: Set error message
        return redirect("/")
    # Store recipe
    recipe = Recipe.create(
        name=request.form['name'],
        grain=request.form['grain'],
        grain_temp=request.form['grain_temp'],
        water=request.form['water'],
        mash_temp=request.form['mash_temp'],
        mash_time=request.form['mash_time'],
        description=request.form['description']
    )
    recipe.save()
    return redirect("/")

# r/badcode
@app.route("/setRelay", methods=["POST"])
def set_relay():
    relay = request.get_json()

    if relay['state']:
        relay['state'] = 0
    else:
        relay['state'] = 1

    if relay['relayName'] == "hlt":
        con.hlt(relay['state'])
        print("HLT switched")
    elif relay['relayName'] == "pump":
        print("pump switched")
        con.pump(relay['state'])

    if relay['state'] == 1:
        relay['state'] = "mash"
    else:
        relay['state'] = "boil"

    if relay['relayName'] == "rimsToMash":
        con.rims_to(relay['state'])
        print("rims_to switched")
    elif relay['relayName'] == "hltToMash":
        print("hlt_to switched")
        con.hlt_to(relay['state'])

    return "True"

@app.route("/allRelaysOff", methods=["POST"])
def all_relays_off():
    con.hlt(0)
    con.pump(0)
    con.hlt_to("boil")
    con.rims_to("boil")
    return "True"

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# API ------------------------------------------------------
# Relay API Resource
@app.route("/relays", methods=["GET"])
def relays():
    relays = [
        {
            "name": "hlt",
            "prettyName": "HLT",
            "status": con.relay_status(con.settings.relays["hlt"])
        },
        {
            "name": "hltToMash",
            "prettyName": "HLT To Mash",
            "status": con.relay_status(con.settings.relays['hltToMash'])
        },
        {
            "name": "rimsToMash",
            "prettyName": "RIMS To Mash",
            "status": con.relay_status(con.settings.relays["rimsToMash"])
        },
        {
            "name": "pump",
            "prettyName": "Pump",
            "status": con.relay_status(con.settings.relays["pump"])
        }
    ]

    return json.dumps(relays)

# PID API Resource
@app.route("/pid", methods=["GET"])
def pid():
    pid = con.pid_status()
    return json.dumps(pid)


if __name__ == '__main__':
    Recipe.create_table(True)
    app.run('0.0.0.0', 8000, extra_files="static/main.js")
