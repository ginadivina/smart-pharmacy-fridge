#!/usr/bin/python3
from flask import Flask
from flask_bootstrap import Bootstrap
app = Flask(__name__)
from app import routes

app.config['SECRET_KEY'] = "secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "secretkey"
bootstrap = Bootstrap(app)