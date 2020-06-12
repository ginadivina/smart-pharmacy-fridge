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
    pressureData = data['Pressure']
    lowPressList = []
    highPressList = []
    humidData = data['Humidity']
    lowHumList = []
    highHumList = []

    print(tempData)
 
    i = 0
    minuteCounter = 0
    while i < len(tempData)-1: # x in tempData
        if tempData[i][3] < "2":
            lowTempList.append(data['Temperature'][i])
            i = i + 1
            if minuteCounter <= 15:
                minuteCounter = 0
                highTempList.clear()
        elif tempData[i][3] >= "8" and tempData[i+1][3] >= "8":
            minuteCounter = minuteCounter + 1
            highTempList.append(data['Temperature'][i])
            i = i + 1
        else:
            i = i + 1
            #No temperature discrepancies
            if minuteCounter <= 15:
                minuteCounter = 0
                highTempList.clear()

    i = 0
    while i < len(humidData)-1:
        if humidData[i][3] > "60":
            highHumList.append(data['Humidity'][i])
            i = i + 1
        elif humidData[i][3] < "0":
            lowHumList.append(data['Humidity'][i])
            i = i + 1
        else:
            i = i + 1

    i = 0
    while i < len(pressureData)-1:
        if int(pressureData[i][3]) > 1080:
            highPressList.append(data['Pressure'][i])
            i = i + 1
        elif int(pressureData[i][3]) < 500:
            lowPressList.append(data['Pressure'][i])
            i = i + 1
        else:
            i = i + 1

    completeDict = {'Low Temperature Alerts': lowTempList, 'High Temperature Alerts': highTempList,
        'Low Humidity Alerts': lowHumList, 'High Humidity Alerts': highHumList,
        'Low Pressure Alerts': lowPressList, 'High Pressure Alerts': highPressList}
    return render_template('report.html', sensor_data=completeDict)

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
