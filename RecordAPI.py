from flask import Flask,request
from flask_restful import Resource, Api,reqparse
from models import db,Bakfile
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

api = Api(app)
# with app.app_context():
#     db.create_all()



@app.route('/')
def hello_world():
    record = Bakfile(ip='z', bakname='a', bakdir='b', md5sum=23, filesize=32, starttime='2019-06-03 23:05:02',
                 stoptime='2019-06-03 23:35:02', costtime=30, incsize=432, mark='xy')

    db.session.add(record)
    db.session.commit()
    return 'Hello World!'

todos = {}
class TodoSimple(Resource):
    def get(self, todo_id):

        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        print(request.form['data'])
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True,host="192.168.74.104")