
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Bakfile(db.Model):
    __tablename__ = 'dbbak'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    ip = db.Column(db.String(20))
    bakname = db.Column(db.String(50))
    bakdir = db.Column(db.String(150))
    md5sum = db.Column(db.String(50))
    filesize = db.Column(db.BigInteger)
    starttime = db.Column(db.DateTime) 
    stoptime = db.Column(db.DateTime)
    costtime = db.Column(db.Integer)
    baktype = db.Column(db.Integer,default=1) #1全量 0增量
    incsize = db.Column(db.BigInteger,nullable=True)
    has_restore = db.Column(db.Integer,default=0) #1有定期还原 0无还原
    to_f01 = db.Column(db.Integer) #1成功 0失败
    to_f01_costtime = db.Column(db.BigInteger,nullable=True)
    mark = db.Column(db.String(20))
    # def __init__(self,ip,bakname, bakdir,md5sum,filesize,starttime,stoptime,costtime,baktype,incsize,has_restore,mark):
    #     self.ip = ip
    #     self.bakname = bakname
    #     self.bakdir = bakdir
    #     self.md5sum = md5sum
    #     self.filesize = filesize
    #     self.starttime = starttime
    #     self.stoptime = stoptime
    #     self.costtime = costtime
    #     self.baktype = baktype
    #     self.incsize = incsize
    #     self.has_restore = has_restore
    #     self.mark = mark
    #
    # def __repr__(self):
    #     return '<bakname %r>' % self.bakname
