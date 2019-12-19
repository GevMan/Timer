from app import db,app
from datetime import date,time,datetime


class user(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(200))
    start_date = db.Column(db.DateTime, default=datetime.now)
    start_time = db.Column(db.String(200))
    day = db.relationship('days',backref='username')

    def __init__(self,*args,**kwargs):
        super(user,self).__init__(*args,**kwargs)

    def __repr__(self):
        return self.username


class days(db.Model):
    id=db.Column(db.Integer,primary_key = True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    day =db.Column(db.String(200))
    work_hours = db.Column(db.String(200))

    def __init__(self,*args,**kwargs):
        super(days,self).__init__(*args,**kwargs)

    def __repr__(self):
        return self.day
