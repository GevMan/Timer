import os
from flask import Flask
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost/timer'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 60
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager=Manager(app)
manager.add_command('db',MigrateCommand)

