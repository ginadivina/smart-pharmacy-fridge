import sqlite3
import os.path

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




