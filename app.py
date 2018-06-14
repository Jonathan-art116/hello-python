from flask import Flask, request
import MySQLdb
import json
from flask import make_response, Response
from flask_sqlalchemy import SQLAlchemy
import mysql
from datetime import datetime
# from flask_json import json_response, FlaskJSON ,JsonTestResponse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/sndb'
db = SQLAlchemy(app)

class Device(db.Model):
    deviceId = db.Column(db.Integer, primary_key=True)
    serialNumber = db.Column(db.String(255), unique=True)
    mac = db.Column(db.String(255), unique=True)
    model = db.Column(db.String(255), nullable=True)
    brand = db.Column(db.String(255), nullable=True)
    operatorSystem = db.Column(db.String(255), nullable=True)
    create_time = db.Column(db.DateTime, nullable=True,default=datetime.now)
    def __init__(self, serialNumber, mac, model, brand, operatorSystem):
        #self.deviceId = deviceId
        self.serialNumber = serialNumber
        self.mac = mac
        self.model = model
        self.brand = brand
        self.operatorSystem = operatorSystem
        #self.create_time = create_time

class Model(db.Model):
    modelId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    def __init__(self, modeId, name):
        self.modelId = modeId
        self.name = name
        #self.create_time = create_time

@app.route('/')
def hello_world():
    return "This is  GET!"

@app.route('/hello')
def hello():
    return 'hello, world'

def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/get/<int:get_data>')
def show_get(get_data):
    return 'Get  %d' % get_data

@app.route('/post', methods=['POST'])
def test():
    if request.method == 'POST'and request.form.get('serialNumber'):
        datax = request.form.to_dict()
        inset = Device(serialNumber=datax['serialNumber'], mac=datax['mac'], model=datax['model'], operatorSystem=datax['operatorSystem'], brand=datax['brand'])
        db.session.add(inset)
        db.session.commit()
        # db.create_all()
        content = str(datax)
        resp = Response_headers(content)
        return resp
    else:
        content = json.dumps({"error_code":"1001"})
        resp = Response_headers(content)
        return resp

@app.errorhandler(403)
def page_not_found(error):
    content = json.dumps({"error_code": "403"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(404)
def page_not_found(error):
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(400)
def page_not_found(error):
    content = json.dumps({"error_code": "400"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(410)
def page_not_found(error):
    content = json.dumps({"error_code": "410"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(500)
def page_not_found(error):
    content = json.dumps({"error_code": "500"})
    resp = Response_headers(content)
    return resp

if __name__ == '__main__':
    db.create_all()
    app.run()