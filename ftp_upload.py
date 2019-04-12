# -*- coding:UTF-8 -*-
import os, ftplib
from ftplib import FTP

bufsize = 1024
ftp=FTP()
ftp.set_debuglevel(2)
timeout = 30
prot = 9999
host = "180.166.175.194"
username = "atel"
password = "Ab123123"
ftp.connect("180.166.175.194",prot,timeout)
ftp.login("atel","Ab123123")
print(ftp.getwelcome())
ftp.cwd("./Test/")
ftp.mkd("rosetta")
ftp.cwd("rosetta")
print(ftp.pwd())

def upload(ftp, filepath):
    f = open(filepath, "rb")
    file_name = os.path.split(filepath)[-1]
    try:
        ftp.storbinary('STOR %s'%file_name, f, bufsize)
        print('成功上传文件： "%s"' % file_name)
    except ftplib.error_perm:
        return False
    return True

if __name__ == "__main__":
    upload(ftp,"C:/test/test.wav")