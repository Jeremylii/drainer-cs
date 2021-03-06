# -*- coding: utf-8 -*-
#
"""
写入随机大小的LOB数据
"""

import random
import string
import os
import subprocess
import mysql.connector
import time
from datetime import date, datetime, timedelta


def crt_blob_file(file_dir="/tmp",file_num=3,file_maxsize_kb=10):
    """
    create blob files.
    """
    for i in range(file_num):
        a = ''.join(random.sample(string.ascii_letters+string.digits,random.randint(3,9)))
        file_name="ddfile_"+a+".dat"
        shellcmd_str="dd if=/dev/zero of=%s/%s bs=1k count=%s" %(file_dir,file_name, random.randint(1,file_maxsize_kb) )
        os.system(shellcmd_str)
    shellcmd_str="ls -l %s" %(file_dir)
    os.system(shellcmd_str)


def crt_clob_str(data_size=100):
    """
    split num
    cn_str:300 letter:60 spe:40
    #25%汉字+25%字母+1%特殊字符
    """
    cn_str = """
TiDB 是 PingCAP 公司自主设计、研发的开源分布式关系型数据库，
是一款同时支持在线事务处理与在线分析处理 (Hybrid Transactional
and Analytical Processing, HTAP) 的融合型分布式数据库产品，
具备水平扩容或者缩容、金融级高可用、实时 HTAP、云原生的分布式数据库、
兼容 MySQL 5.7 协议和 MySQL 生态等重要特性。目标是为用户提供一站式 
OLTP (Online Transactional Processing)、OLAP (Online Analytical Processing)、
HTAP 解决方案。TiDB 适合高可用、强一致要求较高、数据规模较大等各种应用场景
"""
    special_str = """~!@#$%^&*()_++?><:"`-=,./;'[]{}\' 	|'*&$.,/\\"""

    if data_size<400:
        a_size = random.randint(int(data_size/6),int(data_size/4))
        b_size = random.randint(int(data_size/6),int(data_size/4))
        c_size = max(data_size - b_size*3 - a_size, 0)
        print (a_size, b_size, c_size)
        a = ''.join(random.sample(string.ascii_letters+string.digits, a_size))
        b = ''.join(random.sample(cn_str, b_size))
        c = ''.join(random.sample(special_str, c_size))
        comment = "total %s szie, %s normal letters, %s cn letters, %s special letters" %(data_size, a_size, b_size, c_size)
        print (comment)
        return (comment, len(a+b+c), a+b+c)
    else:
        a = ''.join(random.sample(string.ascii_letters+string.digits, 10))
        b = ''.join(random.sample(cn_str, 130))
        c = ''.join(random.sample(special_str, 10))
        mult = int((data_size - 400)/10)
        comment = "total %s szie, %s normal letters, %s cn letters, %s special letters" %(data_size, int(mult*10), 130, 10)
        print (comment)
        return (comment, len(a*mult+b+c), a*mult+b+c)


def insert_blob_data(db_conn={}, data_dir="/tmp" , data_size=10):
    """
    insert blobs

    cnx = mysql.connector.connect(**mys88)
    cursor = cnx.cursor()
    cursor.execute(add_salary, data_salary)
    cnx.commit()
    cursor.close()
    cnx.close()
    """

    crt_blob_file(data_dir, random.randint(1,5), int(data_size/10)*10 )

    WorkDir = data_dir
    FileInfo = {}
    for root, dirs, files in os.walk(WorkDir):
        print(root, dirs, files)
        
    for i in files:
        _filename = WorkDir+"/"+i
        _filesize = os.path.getsize(_filename)
        _SqlName = _filename+" "+str(_filesize)
        print(_filename, _filesize, type(_filename), type(_filesize), _SqlName)
        fp = open(_filename, 'rb')
        img = fp.read()
        add_employee = ("INSERT INTO test.t_blob( b, c, d)  VALUES (  %s, %s, %s)")
        data_employee = (_filename, str(_filesize), img)
        print("insert_mys_data %s %s %s" %("mys81", add_employee, "data_employee"))
        insert_mys_data(mys81,add_employee,data_employee)
        time.sleep(1)

def insert_clob_data(db_conn={}, data_dir="/tmp", data_size=10):
    """
    insert blobs

    cnx = mysql.connector.connect(**mys88)
    cursor = cnx.cursor()
    cursor.execute(add_salary, data_salary)
    cnx.commit()
    cursor.close()
    cnx.close()
    """

    add_employee = ("INSERT INTO test.t_clob(b, c, d)  VALUES (%s, %s, %s)")
    data_employee = crt_clob_str(data_size)
    #data_employee = ("", len(clob_data), clob_data)
    print("insert_mys_data %s %s %s" %("mys81", add_employee, "data_employee"))
    insert_mys_data(mys81, add_employee, data_employee)
    time.sleep(1)


def insert_mys_data(DBUrl="", DynSql="", DynPara=""):
    """
    连接数据库并写入数据
    """
    cnx = mysql.connector.connect(**DBUrl)
    cursor = cnx.cursor()
    #cursor.execute("select now(),version()")
    #for (a,b) in cursor:
        #print(a,b)
    cursor.execute(DynSql, DynPara)
    cnx.commit()
    cnx.close()
    #print(DynSql, DynPara, type(DynSql), type(DynPara))


mys81 = {
    'user' : 'root', 
    'password' : 'sa123456',
    'host' : '172.16.4.81',
    'port' : '4100',
    'database' : 'test',
    'raise_on_warnings' : True
}


#crt_blob_file("/data1/tmp/lob_data",5,1000)
insert_blob_data(mys81, "/data1/tmp/lob_data", random.randint(10,1000))
insert_clob_data(mys81, "/data1/tmp/lob_data", random.randint(1,1000))
#os.system(shellcmd_str)

