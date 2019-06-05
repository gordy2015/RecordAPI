from flask import Flask,request
from flask_restful import Resource, Api,reqparse,fields,marshal_with,marshal,request
from models import db,Bakfile
import config
import datetime

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

api = Api(app)

#如果不存在表就新建此表
# with app.app_context():
#     db.create_all()

# resource_fields = {
#             'ip': fields.String,
#             'bakname': fields.String,
#             'bakdir': fields.String,
#             'md5sum': fields.Integer,
#             'filesize': fields.Integer,
#             'starttime': fields.DateTime(dt_format='rfc822'),
#             'stoptime': fields.DateTime(dt_format='rfc822'),
#             'costtime': fields.Integer,
#             'baktype': fields.Integer(default=0),
#             'has_restore': fields.Integer(default=0),
#             'incsize': fields.Integer,
#             'mark': fields.String
#         }

class Mrecord(Resource):
    # def get(self, **kwargs):
    #     req = request.args.get('last_filesize')
    #     if req:
    #         try:
    #             w = Bakfile.query.order_by(Bakfile.id.desc()).limit(1)
    #             for i in w:
    #                 last_filesize = i.filesize
    #         except:
    #             last_filesize = 0
    #     else:
    #         last_filesize = 0
    #     return last_filesize

    # @marshal_with(resource_fields)
    def post(self,**kwargs):
        r = request.json
        lastf = request.json.get('last_filesize')
        a = request.json.get('ip')
        b = request.json.get('bakname')
        c = request.json.get('bakdir')
        d = request.json.get('md5sum')
        e = request.json.get('filesize')
        f = request.json.get('starttime')
        g = request.json.get('stoptime')
        h = request.json.get('costtime')
        i = request.json.get('incsize')
        j = request.json.get('to_f01')
        k = request.json.get('mark')
        # print(type(r),str(r))
        # t = {'ip': a,'bakname':b}
        #获取上一次的文件大小
        if lastf:
            try:
                w = Bakfile.query.order_by(Bakfile.id.desc()).limit(1)
                for i in w:
                    last_filesize = i.filesize
            except:
                last_filesize = 0
            return last_filesize

        #新增一条记录
        if a and b:
            record = Bakfile(ip=a, bakname=b, bakdir=c, md5sum=d, filesize=e, starttime=f,
                             stoptime=g, costtime=h, incsize=i, to_f01=j, mark=k)
            try:
                db.session.add(record)
                db.session.commit()
                code = 200
                result = "RECORD SUCCESS"
            except Exception as e:
                result = "RECORD FAILE"
                code = 600
        else:
            result = "not ip and bakname"
            code = 601
        return result,code

api.add_resource(Mrecord, '/mrecord')

if __name__ == '__main__':
    app.run(debug=True,host="192.168.100.254")