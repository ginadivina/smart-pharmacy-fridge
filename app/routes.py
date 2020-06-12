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

    pressure_data = data['Pressure']
    low_press_list = []
    high_press_list = []

    humid_data = data['Humidity']
    low_humid_list = []
    high_humid_list = []
 
    minuteCounter = 0
    for index, reading in enumerate(temp_data):
        if reading[3] < "2":
            low_temp_list.append(data['Temperature'][index])
            if minuteCounter <= 15:
                minuteCounter = 0
                high_temp_list.clear()
        elif reading[3] >= "8" and temp_data[i+1][3] >= "8":
            minuteCounter = minuteCounter + 1
            high_temp_list.append(data['Temperature'][index])
        else:
            #no anomilies
            if minuteCounter <= 15:
                minuteCounter = 0
                high_temp_list.clear()

    for index, reading in enumerate(humid_data):
        if reading[3] > "60":
            high_humid_list.append(data['Humidity'][index])
        elif reading[3] < "0":
            low_humid_list.append(data['Humidity'][index])

    for index, reading in enumerate(pressure_data):
        if int(reading[3]) > 1080:
            high_press_list.append(data['Pressure'][index])
        elif int(reading[3]) < 500:
            low_press_list.append(data['Pressure'][index])

    completeDict = {'Low Temperature Alerts': low_temp_list, 'High Temperature Alerts': high_temp_list,
        'Low Humidity Alerts': low_humid_list, 'High Humidity Alerts': high_humid_list,
        'Low Pressure Alerts': low_press_list, 'High Pressure Alerts': high_press_list}
    return render_template('report.html', sensor_data=completeDict)


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
