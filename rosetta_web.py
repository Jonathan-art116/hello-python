from flask import Flask,abort
from flask import render_template
from flask_bootstrap import Bootstrap
import MySQLdb
import time

app = Flask(__name__)
bootstrap = Bootstrap(app)

database_host = 'localhost'	#change the host you need to use
database_user = 'root'	#change the database user 
database_password = 'root'	#change the database password
database_db_name = 'sndb'	#change the database name, the database name need to be created in Mysql
db = MySQLdb.connect(host=database_host,user=database_user,password=database_password,db=database_db_name)
cursor = db.cursor()
creat = "CREATE TABLE IF NOT EXISTS " + 'ROSETTA_WEB' + "(" \
            + "ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
            + "SN CHAR(20) NOT NULL,UNIQUE(SN)," \
            + "Build CHAR(20)," \
            + "Version CHAR(60), " \
            + "Createtime datetime DEFAULT CURRENT_TIMESTAMP)"

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
    	updata_funtion(Version,SN)
    	return "Add Device Successful."
    else:
    	return abort(404)

def add_devices(SN,Build,Version):
	insert = "INSERT INTO ROSETTA_WEB" + "(SN, Build, Version)" + " VALUES('"+ SN +"','"+ Build +"','"+ Version +"')"
	try:
		cursor.execute(insert)
		db.commit()
	except:
		db.rollback()

#update the funtion_table's version
def updata_funtion(Version,SN):
	updata = "UPDATE ROSETTA_FUNCTION SET Version='%s'" % (Version) + "WHERE SN='%s'" % (SN)
	try:
		cursor.execute(updata)
		db.commit()
	except:
		db.rollback()


#check function database
def check_device(SN):
	check_device = "select * from ROSETTA_FUNCTION where SN = '%s'" % (SN)
	cursor.execute(check_device)
	result = cursor.fetchone()
	if result is None:
		return True
	return False

#check the new database
def check_sn(SN):
	check_sn = "select * from ROSETTA_WEB where SN = '%s'" % (SN)
	cursor.execute(check_sn)
	result = cursor.fetchone()
	if result is None:
		return True
	return False

@app.route('/show_devices')
def index():
    time.sleep( 5 )
    show_devices = "select * from rosetta_web order by ID DESC limit 0, 10"
    cursor.execute(show_devices)
    u = cursor.fetchall()
    return render_template('index.html',u=u)

if __name__ == '__main__':
	db.close()
	app.run(debug=True)
