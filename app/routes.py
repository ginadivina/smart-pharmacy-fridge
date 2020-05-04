from flask import redirect, render_template, request, jsonify
from app import app
from app.database import get_sensors, get_medicine_stock, write_sensor_log


@app.route('/')
def index():
    data = get_medicine_stock()
    return render_template('base.html', medicine_stock_data=data)


@app.route('/sensors')
def sensors():
    data = get_sensors()
    return render_template('sensors.html', sensor_data=data)

@app.route('/api/sensor', methods=['POST'])
def write_sensors():
    sensordata = request.json
    sensor_type_id = sensordata['sensor_type_id'] #placeholder to test, this variable is getting the data from the sensors
    datetime = sensordata['datetime'] #placeholder to test
    value = sensordata['value'] #placeholder to test

    write_sensor_log(sensor_type_id, datetime, value)
    
    data = get_sensors()
    return render_template('sensors.html', sensor_data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
