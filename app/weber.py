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


# Routes

@app.route("/")
def index():
    recipes = Recipe.select()
    return render_template("index.html", recipes=recipes)

@app.route("/controller")
def controller():
    return render_template("controller.html")

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

@app.route("/pid", methods=["GET"])
def pid():
    pid = con.pid_status()
    return json.dumps(pid)

# r/badcode
def toggleRelay(name, state):
    if name == "hlt":
        if state == "True":
            con.hlt(1)
        else:
            con.hlt(0)

    if name == "pump":
        if state == "True":
            con.pump(0)
        else:
            con.pump(1)

    # TODO: Maybe invert this?
    if name == "rimsToMash":
        if state == "True":
            con.rims_to("boil")
        else:
            con.rims_to("mash")

    if name == "hltToMash":
        if state == "True":
            con.hlt_to("boil")
        else:
            con.hlt_to("mash")

    return True

@app.route("/toggleRelay", methods=["POST"])
def handleToggleRelayPost():
    toggleRelay(request.get_json()['relayName'], request.get_json()['status'])
    return "True"

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

@app.route('/post', methods=["POST"])
def accept_post():
    print(request.form)
    return render_template("controller.html")


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


if __name__ == '__main__':
    Recipe.create_table(True)
    app.run('0.0.0.0', 8000, extra_files="static/main.js")
