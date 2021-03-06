from flask import redirect, render_template, request, jsonify
from app import app
from app.database import get_sensors, get_medicine_stock, write_sensor_log, get_user, get_users, write_users, \
    write_user_encoding, get_user_encodings, update_medicine_log, unlock_door, lock_door
from app.forms import newUserForm
from werkzeug.utils import secure_filename
import face_recognition
import os
import requests
import json
import numpy as np

fridge_port_number = None


@app.route('/')
def index(authorisedUser=False, authorisedUserId=False, photo=False, access_id=False):
    data = get_medicine_stock()
    medicine_dict = {}
    print(authorisedUser, authorisedUserId, photo)
    if authorisedUser and authorisedUserId and photo:
        fridge_border="4px solid green"
    else:
        fridge_border="4px solid orangered"

    for medicine in data:
        medicine_dict[medicine[4]] = int(medicine[2])
    return render_template('index.html', medicine_stock_data=data, medicine_dict=medicine_dict, fridge_border=fridge_border,
        authorisedUser=authorisedUser, authorisedUserId=authorisedUserId, photo=photo, access_id=access_id)


@app.route('/report')
def report():
    data = get_sensors()
    temp_data = data['Temperature']
    low_temp_list = []
    high_temp_list = []

    for index, reading in enumerate(temp_data):
        if reading[3] == "20":  # placeholder temperature for testing, change to: if tempData[i][3] < "2":
            low_temp_list.append(data['Temperature'][index])
        elif reading[3] == "20.1":  # placeholder temperature for testing, change to: if tempData[i][3] > "8":
            high_temp_list.append(data['Temperature'][index])

    temp_dict = {'Low Temperature Alerts': low_temp_list, 'High Temperature Alerts': high_temp_list}
    return render_template('report.html', sensor_data=temp_dict)


@app.route('/dashboard')
def dashboard():
    data = get_sensors()
    return render_template('dashboard.html', sensor_data=data)


@app.route('/api/sensor', methods=['POST'])
def write_sensors():
    sensor_data = request.json
    sensor_type_id = sensor_data[
        'sensor_type_id']  # placeholder to test, this variable is getting the data from the sensors
    datetime = sensor_data['datetime']  # placeholder to test
    value = sensor_data['value']  # placeholder to test

    write_sensor_log(sensor_type_id, datetime, value)

    data = get_sensors()
    return render_template('dashboard.html', sensor_data=data)


@app.route('/api/newClient')
def newClient():
    global fridge_port_number
    requestData = request.json
    fridge_port_number = requestData['port']
    return 'Fridge connected to server'


@app.route('/auth')
def triggerAuth():
    try:
        global fridge_port_number
        url = 'http://127.0.0.1:' + str(fridge_port_number)
        headers = {'Content-type': 'text/html; charset=UTF-8'}
        # See if it would be possible to redirect to a processing page during this time
        response = requests.post(url, data="login", headers=headers)
        response_dict = json.loads(response.text)
        encoding = response_dict["encoding"]
        knownEncodings = get_user_encodings()
        authorisedUser = checkForMatch(encoding, knownEncodings)
        if authorisedUser is None:
            return index(authorisedUser=None)

        # get the name and the file path of the user's photo
        authorisedUser = get_user(authorisedUser)
        # log the access
        access_id = unlock_door(authorisedUser[0][2])
        return index(authorisedUser=authorisedUser[0][0], authorisedUserId=authorisedUser[0][2], photo=authorisedUser[0][1], access_id=access_id)
    
    except Exception as error:
        # access_id = unlock_door("13")
        # return index(authorisedUser="Tristan", authorisedUserId="13", photo="IMG_1909.jpg", access_id=access_id) # Used for testing without face_recognition
        return index(authorisedUser=None)


# This route should provide all the administrative information and transactions
# currently only providing users (of which we have none lol!)
@app.route('/admin', methods=['GET', 'POST'])
def userAdmin():
    form = newUserForm()
    if form.validate_on_submit():
        name = form.name.data
        file = request.files['file']
        filename = secure_filename(file.filename)
        thisDir = os.path.dirname(__file__)
        file.save(os.path.join(thisDir, 'static', 'user_photos', filename))
        userID = write_users(name, filename)
        faceEncoding = encodePhoto(filename)
        write_user_encoding(userID, faceEncoding)

        form = newUserForm()
    data = get_users()
    return render_template('admin.html', form=form, data=data)


@app.route('/update_medicine_stock/<authorisedUserId>/<access_id>', methods=['POST'])
def update_medicine_stock(authorisedUserId, access_id):  # Our main search page interface
    if request.method == 'POST':
        values = request.form.to_dict()
        for medicine in values:
            update_medicine_log(authorisedUserId, medicine, values[medicine])
        # Lock the door and log it
        lock_door(access_id)
        return index()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


################################
# Helper functions
################################

def encodePhoto(filename):
    thisDir = os.path.dirname(__file__)
    image = face_recognition.load_image_file(os.path.join(thisDir, 'user_photos', filename))
    imageEncodings = face_recognition.face_encodings(image)[0]
    return imageEncodings


def checkForMatch(faceEncoding, knownEncodings):
    # knownEncodings is a list of tuples, with the User ID followed by the encoding.
    # We need to convert to a list of lists, extracting the User ID
    encodingList = []
    UIDs = []
    for encoding in knownEncodings:
        encoding = list(encoding)
        userID = encoding.pop(0)
        encoding = np.array(encoding)
        encodingList.append(encoding)
        UIDs.append(userID)
    # compare the faces
    matchedFaces = face_recognition.compare_faces(encodingList, np.array(faceEncoding))
    if True in matchedFaces:
        index = matchedFaces.index(True)
        return UIDs[index]
    return None
