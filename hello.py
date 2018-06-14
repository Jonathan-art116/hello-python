#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from flaskext.mysql import MySQL
import json
import time

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'atel13579'
app.config['MYSQL_DATABASE_DB'] = 'DeviceData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL()
mysql.init_app(app)

@app.route("/")
def hello():
    return "Hello, this is demo only! --2--\n"

@app.route("/activate", methods=["POST"])
def activate():
    ret = {}
    try:
        rd = request.get_data()
        if rd is None or len(rd) == 0:
            ret["status"] = -1
            return json.dumps(ret)
        jd = json.loads(rd)
        print jd
        if jd is None:
            ret["status"] = -2
            return json.dumps(ret)
        if not jd.get('serialNumber') or len(jd['serialNumber']) == 0:
            ret["status"] = -3
            return json.dumps(ret)
        sn = jd['serialNumber']
        if check_sn(sn):
            ret["status"] = 1
            return json.dumps(ret)
        if not jd.get('model') or len(jd['model']) == 0:
            ret["status"] = -4
            return json.dumps(ret)
        model = jd['model']
        if not jd.get('brand') or len(jd['brand']) == 0:
            ret["status"] = -5
            return json.dumps(ret)
        brand = jd['brand']
        if not jd.get('operatorSystem') or len(jd['operatorSystem']) == 0:
            ret["status"] = -6
            return json.dumps(ret)
        os = jd['operatorSystem']
        mac = ""
        if jd.get('macAddress'):
            mac = jd['macAddress']
        imei = ""
        if jd.get('imei'):
            imei = jd['imei']
        ret["status"] = add_device(sn, model, brand, os, mac, imei)
        return json.dumps(ret) 
    except Exception, e:
        print e
        ret["status"] = -100
        ret["message"] = e.message
        return json.dumps(ret)

@app.route("/query", methods=["POST"])
def query():
    ret = {}
    try:
        rd = request.get_data()
        if rd is None or len(rd) == 0:
            ret["status"] = -1
            return json.dumps(ret)
        jd = json.loads(rd)
        print jd
        if jd is None:
            ret["status"] = -2
            return json.dumps(ret)
        if not jd.get('serialNumber') or len(jd['serialNumber']) == 0:
            ret["status"] = -3
            return json.dumps(ret)
        sn = jd['serialNumber']
        if check_sn(sn):
            ret["status"] = 1
            return json.dumps(ret)
        ret["status"] = 0
        return json.dumps(ret)
    except Exception, e:
        print e
        ret["status"] = -100
        ret["message"] = e.message
        return json.dumps(ret)

def check_sn(sn):
    cursor = mysql.connect().cursor()
    cursor.execute('select * from Device where serialNumber="' + sn + '"')
    data = cursor.fetchone()
    if data is None:
        return False
    return True

def add_device(sn, model, brand, os, mac, imei):
    database = mysql.connect()
    mid = get_item_id(database, 'Model', model)
    bid = get_item_id(database, 'Brand', brand)
    oid = get_item_id(database, 'OperatorSystem', os)
    dt = time.strftime('%Y-%m-%d %X', time.localtime())
    key = 'serialNumber,model,brand,operatorSystem,datetime,macAddress,imei'
    value = '"%s",%d,%d,%d,"%s","%s","%s"' % (sn, mid, bid, oid, dt, mac, imei) 
    print 'key = ' + key + ', value = ' + value
    cursor = database.cursor()
    cursor.execute('insert into Device(' + key + ') values (' + value + ')')
    database.commit()
    return 0

def get_item_id(database, table, name):
    cursor = database.cursor()
    cursor.execute('select * from ' + table + ' where name="' + name + '"')
    data = cursor.fetchone()
    if data is None:
        cursor.execute('insert into ' + table + '(name,count) values ("' + name + '",1)')
        database.commit()
        cursor.execute('select * from ' + table + ' where name="' + name + '"')
        data = cursor.fetchone()
    else:
        cursor.execute('update ' + table + ' set count = count + 1 where name="' + name + '"')
        database.commit()
    print data
    return data[0];

if __name__ == "__main__":
    app.run(debug=True)
