import numpy as np 
import datetime as dt 

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#database setup 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement 
station = Base.classes.measurement 

#create session 
session = Session(engine)

#flask setup and routes 
app = Flask(__name__)

@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[last_date format:yyyy-mm-dd]<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    prcp_results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-24").\
        all()

    session.close()

    prcp_list = []
    for date, prcp in prcp_results: 
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp 

        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    sta_results = session.query(station.station).\
                    order_by(station.station).all()
    
    session.close()

    sta_list = list(np.ravel(sta_results))
    return jsonify(sta_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    tobs_results = session.query(measurement.date, measurement.tobs, measurement.prcp).\
                    filter(measurement.date >= '2016-08-23').\
                    filter(measurement.station == 'USC00519281').\
                    order_by(measurement.date).all()
    
    session.close()

    tobs_list = []
    for prcp, date, tobs in tobs_results: 
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        tobs_list.append(tobs_dict)
    
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):

    session = Session(engine)
    start_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                        filter(measurement.date >= start_date).all()
    
    session.close()

    start_date_tobs = []
    for min, avg, max in results: 
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min 
        start_date_tobs_dict["avg temp"] = avg
        start_date_tobs_dict["max_temp"] = max  

        start_date_tobs.append(start_date_tobs_dict)
    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start_date>/<last_date>")
def Start_end_date(start_date, last_date):
    session = Session(engine)

    all_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    all_tobs = []
    for min, avg, max in results:
        all_tobs_dict = {}
        all_tobs_dict["min_temp"] = min
        all_tobs_dict["avg_temp"] = avg
        all_tobs_dict["max_temp"] = max
        all_tobs.append(all_tobs_dict) 
    

    return jsonify(all_tobs)

if __name__ == "__main__":
    app.run(debug=True)