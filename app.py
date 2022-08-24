from datetime import datetime
from enum import unique
from webbrowser import get
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


# Running this API:
# flask run --port 4000


# Runs

class Runs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    runs = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.runs}"

@app.route('/cricket/runs/', methods=['GET'])
def get_runs():
    runs = Runs.query.all()

    output = []
    for runs in runs:
        run_data = {'runs': runs.runs}
        output.append(run_data)
    return {"runs": output}

@app.route('/cricket/runs/<id>', methods=['GET'])
def get_runs_search(id):
    runs = Runs.query.get_or_404(id)
    return {"runs": runs.runs}

@app.route('/cricket/runs/', methods=['POST']) 
def add_runs():
    runs = Runs(runs=request.json['runs'])
    db.session.add(runs)
    db.session.commit()
    return {'runs_added': runs.runs}

@app.route('/cricket/runs/<id>', methods=['DELETE'])
def delete_runs(id):
    runs = Runs.query.get(id)
    if runs is None:
        return {"error": "not found"}
    db.session.delete(runs)
    db.session.commit()
    return {"message": "runs was deleted"}      
   





# Misc

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
    return {"message": 'Welcome to the Spherical API. Please return help for help.'}

@app.route('/help')
def help():
    return {
        "run_endpoints": "/runs/ GET - Request set of Runs from the CricCounter App.     /runs/<id> GET - Request set of runs via ID    /runs/ POST - Post new record of runs    /runs/<id> DELETE - Delete run records via ID. ",
        "drinks_endpoints": "Coming Soon.",
        "message": 'Welcome to the Spherical API. Below are current endpoints',
        }


@app.route('/misc/drinks/', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, "description": drink.description}
        output.append(drink_data)
    return {"drinks": output}

@app.route('/misc/drinks/<id>', methods=['GET'])
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}

@app.route('/misc/drinks/', methods=['POST']) 
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

@app.route('/misc/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message": "drink was deleted"}    