from flask import Flask, jsonify


import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

engine = create_engine("sqlite:///./hawaii.sqlite") 

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


# Routes

@app.route('/')
def home():
  return (
      f"Routes:<br/>"
      f"/api/v1.0/precipitation<br/>"
      f"/api/v1.0/stations<br/>"
      f"/api/v1.0/tobs<br/>"
      f"/api/v1.0/start and /api/v1.0/start/end<br/>"
  )


@app.route('/api/v1.0/precipitation')
def precipitation_query():
  precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23')
  
  precipitation_data = precipitation.all()
  print(precipitation_data)
  
  return jsonify(precipitation_data)


@app.route('/api/v1.0/stations')
def station_query():
  
  session.query(func.count(Station.station)).all()

  station_counts = (session.query(Measurement.station, func.count(Measurement.station))
                        .group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all())
  
  print(station_counts)
  
  return jsonify(station_counts)


@app.route('/api/v1.0/<start>')
def temperature_start(start=None):
  print('start date:', start)

  temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

  return jsonify(temp_data)


@app.route('/api/v1.0/<start>/<end>')
def temperature_start_end(start=None, end=None):
  print('start date:', start)
  print('end date:', end)

  temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

  return jsonify(temp_data)

# Run app
if __name__ == '__main__':
    app.run()