from flask import redirect, render_template, request, jsonify
from app import app
from app.database import get_sensors, get_medicine_stock, write_sensor_log


@app.route('/')
def index():
    data = get_medicine_stock()
    return render_template('base.html', medicine_stock_data=data)


@app.route('/report')
def report():
    data = get_sensors()
    temp_data = data['Temperature']
    low_temp_list = []
    high_temp_list = []

    for index, reading in enumerate(temp_data):
        if reading[3] == "20":  #placeholder temperature for testing, change to: if tempData[i][3] < "2":
            low_temp_list.append(data['Temperature'][index])
        elif reading[3] == "20.1":  #placeholder temperature for testing, change to: if tempData[i][3] > "8":
            high_temp_list.append(data['Temperature'][index])

    temp_dict = {'Low Temperature Alerts': low_temp_list, 'High Temperature Alerts': high_temp_list}
    return render_template('report.html', sensor_data=temp_dict)


@app.route('/sensors')
def sensors():
    data = get_sensors()
    return render_template('sensors.html', sensor_data=data)


@app.route('/api/sensor', methods=['POST'])
def write_sensors():
    sensor_data = request.json
    sensor_type_id = sensor_data['sensor_type_id'] #placeholder to test, this variable is getting the data from the sensors
    datetime = sensor_data['datetime'] #placeholder to test
    value = sensor_data['value'] #placeholder to test

    write_sensor_log(sensor_type_id, datetime, value)
    
    data = get_sensors()
    return render_template('sensors.html', sensor_data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
