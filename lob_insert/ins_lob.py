#
# insert LoB data

import mysql.connector
from datetime import date, datetime, timedelta
import os
import sys
import subprocess


def insert_mys_data(DBUrl="", DynSql="", DynPara=""):
    '''连接数据库并写入数据 '''
    cnx = mysql.connector.connect(**DBUrl)
    cursor = cnx.cursor()
    #cursor.execute("select now(),version()")
    #for (a,b) in cursor:
        #print(a,b)
    cursor.execute(DynSql, DynPara)
    cnx.commit()
    cnx.close()
    #print(DynSql, DynPara, type(DynSql), type(DynPara))

WorkDir = "/data1/tmp/lob_insert"
FileInfo = {}

mys81 = {
    'user' : 'findpt',
    'password' : 'xxxx',
    'host' : 'xxx.xx.xx.xx',
    'port' : '3306',
    'database' : 'findpt',
    'raise_on_warnings' : True
}


for root, dirs, files in os.walk(WorkDir):
    print(root, dirs, files)

for i in files:
    _filename = WorkDir+"/"+i
    _filesize = os.path.getsize(_filename)
    _SqlName = _filename+" "+str(_filesize)
    print(_filename, _filesize, type(_filename), type(_filesize), _SqlName)
    fp = open(_filename, 'rb')
    img = fp.read()
    img = _filename
    add_employee = ("INSERT INTO findpt.t_clob( b, c)  VALUES (  %s, %s)")
    data_employee = (_SqlName,img)
    #print("insert_mys_data %s %s %s" %(mys81,add_employee,data_employee))
    insert_mys_data(mys81,add_employee,data_employee)
    print("---insert_mys_data %s ---" %(_SqlName))
