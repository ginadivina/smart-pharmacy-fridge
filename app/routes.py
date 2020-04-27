from flask import redirect, render_template
from app import app
from app.database import get_sensors, get_medicine_stock


@app.route('/')
def index():
    data = get_medicine_stock()
    return render_template('base.html', medicine_stock_data=data)


@app.route('/sensors')
def sensors():
    data = get_sensors()
    return render_template('sensors.html', sensor_data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
