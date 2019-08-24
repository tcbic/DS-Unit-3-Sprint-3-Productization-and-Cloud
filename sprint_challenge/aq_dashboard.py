"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

api = openaq.OpenAQ()

def retrieve_data():
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    data_tuple_list = [(item['date']['utc'], item['value']) for item in body['results']]
    return data_tuple_list

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time: %s --- Value: %s>' % (self.datetime, self.value)   

@APP.route('/')
def root():
    """Base view."""
    filtered = Record.query.filter(Record.value >= 10).all()
    return render_template('layout.html', filtered=filtered)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data_tuple_list = retrieve_data()
    for i, values in enumerate(data_tuple_list):
        record = Record(id=i, datetime=values[0],
                            value=values[1])
        DB.session.add(record)
    DB.session.commit() 
    
    return 'Data refreshed!'