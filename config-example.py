from flask import Flask
import os,sqlite3
from flask_sqlalchemy import SQLAlchemy

Flask.debug = True

Flask.reload = True

# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqilte://' + os.path.join(basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:passwd@192.168.0.1:3360/testdb"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True