from flask import Flask
import time
import MySQLdb

app = Flask(__name__)
db = MySQLdb.connect(host='localhost',user='root',password='root',db='sndb')
cursor = db.cursor()
creat = "CREATE TABLE IF NOT EXISTS " + 'ROSETTA_WEB' + "(" \
            + "SN CHAR(20) NOT NULL,UNIQUE(SN)," \
            + "Build CHAR(20)," \
            + "Version CHAR(20), " \
            +"Createtime datetime DEFAULT CURRENT_TIMESTAMP)"

cursor.execute(creat)

@app.route('/test')
def hello_world():
    return 'Hello,World!'

@app.route('/<path:subpath>')
def show_subpath(subpath):
    data = subpath
    grap = data.split("/",3)
    SN = grap[0]
    Build = grap[1]
    Version = grap[2]
    if check_sn(SN) == True and check_device(SN) == False:
    	add_devices(SN,Build,Version)
    	return "Add Device Successful."
    else:
    	return "The device already exists Or please complete the functional test."

def add_devices(SN,Build,Version):
	insert = "INSERT INTO ROSETTA_WEB" + "(SN, Build, Version)" + " VALUES('"+ SN +"','"+ Build +"','"+ Version +"')"
	try:
		cursor.execute(insert)
		db.commit()
	except:
		db.rollback()

def check_device(SN):
	check_device = "select * from ROSETTA_FUNCTION where SN = '%s'" % (SN)
	cursor.execute(check_device)
	result = cursor.fetchone()
	if result is None:
		return True
	return False


def check_sn(SN):
	check_sn = "select * from ROSETTA_WEB where SN = '%s'" % (SN)
	cursor.execute(check_sn)
	result = cursor.fetchone()
	if result is None:
		return True
	return False


if __name__ == '__main__':
	db.close()
	app.run(debug=True)
