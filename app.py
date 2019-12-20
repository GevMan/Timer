
import os
from flask import Flask
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://mfeyq8tq95ldf7g3:ld1ic4nbalv55wv4@f8ogy1hm9ubgfv2s.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/j962xvujyevc1gxk'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 60
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager=Manager(app)
manager.add_command('db',MigrateCommand)

