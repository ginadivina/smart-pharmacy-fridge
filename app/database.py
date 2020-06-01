import sqlite3
import os.path
import numpy as np
import uuid
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "db.db")


def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        db = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return db


def get_sensors():
    try:
        data = {}
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT sensor_type_id, name FROM sensor_log LEFT JOIN sensor_types ON sensor_log.sensor_type_id=sensor_types.id")
        distinct = cursor.fetchall()  # Retrieve all results
        for sensor in distinct:
            cursor.execute("SELECT * FROM sensor_log WHERE sensor_type_id = ?", (sensor[0],))
            sensor_data = cursor.fetchall()  # Retrieve all results
            data[sensor[1]] = sensor_data

        return data

    except Exception as e:
        print(e)
        return e


def get_medicine_stock():
    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM medicine_stock LEFT JOIN medicine_types on medicine_stock.medicine_type_id=medicine_types.id")
        data = cursor.fetchall()  # Retrieve all results

        return data
    
    except Exception as e:
        print(e)
        return e

def update_medicine_log(authorisedUserId, medicine_type_id, new_stock):
    try:
        log_id = str(uuid.uuid4())
        log_datetime = datetime.datetime.now()
        db = create_connection()
        cursor = db.cursor()

        cursor.execute("SELECT value FROM medicine_stock where medicine_type_id=?", (medicine_type_id,))
        current_stock = cursor.fetchall()  # Retrieve all results
        change_in_stock = int(new_stock) - int(current_stock[0][0])
        if change_in_stock == 0:
            return
            
        # Add a new medicine_log entry
        cursor.execute("INSERT INTO medicine_log (id, medicine_type_id, datetime, value, user_id) VALUES (?, ?, ?, ?, ?)", (log_id, medicine_type_id, log_datetime, change_in_stock, authorisedUserId))
        db.commit()
        # Update current stock
        cursor.execute("UPDATE medicine_stock set value=? where medicine_type_id=?", (int(new_stock), medicine_type_id))
        db.commit()
        return
    
    except Exception as e:
        print(e)
        return e


def write_sensor_log(sensor_type_id, datetime, value):
    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO sensor_log (sensor_type_id, datetime, value) VALUES (?, ?, ?)", (sensor_type_id, datetime, value))
        db.commit()
        return cursor.lastrowid       

    except Exception as e:
        print(e)
        return e

def get_user(id):
    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("SELECT name, photo_path, user_id FROM users WHERE user_id = ?", (id,))
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(e)
        return e

def get_users():
    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("SELECT user_id, name FROM users")
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(e)
        return e

def write_users(name, filename):
    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, photo_path) VALUES (?, ?)", (name, filename))
        db.commit()
        return cursor.lastrowid
    except Exception as e:
        print(e)
        return e

def write_user_encoding(ID, encodings):
    try:
        row = list(encodings)
        row.insert(0,ID)
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO user_id_encoding VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (row))
        db.commit()
        return
    except Exception as e:
        print(e)
        return e

def get_user_encodings():
    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user_id_encoding")
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(e)
        return e