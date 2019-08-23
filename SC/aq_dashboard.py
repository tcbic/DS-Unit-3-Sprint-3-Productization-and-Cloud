"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
import openaq
import requests
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

api = openaq.OpenAQ()

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time: {} --- Value: {}>'.format(self.datetime, self.value)

@APP.route('/')
def root():
    """Base view."""
    return_list = process_results()
    list_string = str(return_list)
    filtered_values = Record.query.filter(Record.value >= 10).all()
    return render_template('layout.html', filtered_values=filtered_values)

def process_results():
    list_a = []
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for result in range(len(body['results'])):
        tup = (body['results'][result]['date']['utc'], body['results'][result]['value'])
        list_a.append(tup)
        output = Record(datetime=str(tup[0]), value=tup[1])
        DB.session.add(output)
        DB.session.commit()
    return list_a
