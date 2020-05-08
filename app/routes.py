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
    tempData = data['Temperature']
    lowTempList = []
    highTempList = []
 
    i = 0
    for x in tempData:
        if tempData[i][3] == "20":  #placeholder temperature for testing, change to: if tempData[i][3] < "2":
            lowTempList.append(data['Temperature'][i])
            i = i + 1
        elif tempData[i][3] == "20.1":  #placeholder temperature for testing, change to: if tempData[i][3] > "8":
            highTempList.append(data['Temperature'][i])
            i = i + 1
        else:
            i = i + 1
            #No temperature discrepancies

    tempDict = {'Low Temperature Alerts': lowTempList, 'High Temperature Alerts': highTempList}
    return render_template('report.html', sensor_data=tempDict)

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
