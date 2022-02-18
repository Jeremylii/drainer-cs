# -*- coding: utf-8 -*-
#
"""
查询Mysql/Oracle的数据，并输入文件
当前用于比较Mys和Ora的表数目
"""

import random
import string
import os
import subprocess
import mysql.connector
import cx_Oracle
import time
from datetime import date, datetime


def select_mys_data_to_file(DBUrl="", DynSql="", DynPara=(), FileName=""):
    """
    查询数据并写入csv文件
    """
    cnx = mysql.connector.connect(**DBUrl)
    cursor = cnx.cursor()
    cursor.execute(DynSql)
    
    #for (table_schema, table_name, table_type, create_time) in cursor:
    for (data) in cursor:
        #print(type(data), len(data), data)
        f_write_file(FileName, str(data)+"\n")
        #print("%s,%s,%s,%s" %(table_schema, table_name, table_type, create_time.strftime('%Y-%m-%d %H:%M:%S') ))
        #data = table_schema+','+table_name+','+table_type+','+create_time.strftime('%Y-%m-%d %H:%M:%S')
        #f_write_file("mys_tab.txt", data+"\n")
    cursor.close()
    cnx.close()

def select_ora_data_to_file(DBUrl="", DynSql="", DynPara=(), FileName=""):
    """
    查询数据并写入csv文件
    """
    cnx = cx_Oracle.connect(user="ljs_20211207",
        password="ljs_20211207",
        dsn="172.16.4.87:1521/gbk")
    cursor = cnx.cursor()
    cursor.execute(DynSql)
    
    #for (table_schema, table_name, table_type, create_time) in cursor:
    for (data) in cursor:
        #print(type(data), len(data), data)
        f_write_file(FileName, str(data)+"\n")
        #print("%s,%s,%s,%s" %(table_schema, table_name, table_type, create_time.strftime('%Y-%m-%d %H:%M:%S') ))
        #data = table_schema+','+table_name+','+table_type+','+create_time.strftime('%Y-%m-%d %H:%M:%S')
        #f_write_file("mys_tab.txt", data+"\n")
    cursor.close()
    cnx.close()

def select_ora_lobdata_to_file(DBUrl="", DynSql="", DynPara=(), FileName=""):
    """
    查询数据并写入csv文件
    dbms_metadata.get_ddl返回的是LOB数据
    """
    cnx = cx_Oracle.connect(user="ljsuser",
        password="ljspassword",
        dsn="172.16.4.87:1521/oratidb")
    cursorlob = cnx.cursor()
    cursorlob.execute(DynSql)
    #rows = cursorlob.fetchall()
    for row in cursorlob:
        f = open(FileName, mode="wb+")
        f.write(row[0][0])
        f.close()

    #for (table_schema, table_name, table_type, create_time) in cursor:
    #print(type(rows), len(rows), type(rows[0]), type(rows[0][0]))
    #print(rows[0][0])
        #r = data[0][0].read()
        #print(r)
        #f_write_file(FileName, r+"\n")
        #print("%s,%s,%s,%s" %(table_schema, table_name, table_type, create_time.strftime('%Y-%m-%d %H:%M:%S') ))
        #data = table_schema+','+table_name+','+table_type+','+create_time.strftime('%Y-%m-%d %H:%M:%S')
        #f_write_file("mys_tab.txt", data+"\n")
    cursorlob.close()
    cnx.close()

def f_write_file(file_name="", data=""):
    fp = open(file_name, mode="a", encoding="utf-8")
    fp.write(data)
    fp.close

#mysql
mys81 = {
    'user' : 'root', 
    'password' : 'sa123456',
    'host' : '172.16.4.81',
    'port' : '4100',
    'database' : 'test',
    'buffered' : True,
    'raise_on_warnings' : True
}

tab_schema = "ts_coms"
return_datahead = ("table_schema", "table_name", "table_type", "create_time",)
mys_query_sum = "select table_schema,count(1) from information_schema.tables where table_schema='%s' group by table_schema" %(tab_schema)
mys_query_detail = "select upper(table_schema),upper(table_name) from information_schema.tables where table_schema='%s' order by table_schema,table_name"  %(tab_schema)

#select_mys_data_to_file(DBUrl=mys81, DynSql=mys_query_sum, FileName="mys_tab.txt")
#select_mys_data_to_file(DBUrl=mys81, DynSql=mys_query_detail, FileName="mys_tab.txt")

#oracle 
ora87gbk = {
    'user' : 'ljs_20211207', 
    'password' : 'ljs_20211207',
    'host' : '172.16.4.87',
    'port' : '1521',
    'sid' : 'gbk'
}

tab_schema = "ts_coms"
ora_query_sum = "select owner,object_type,count(1) from dba_objects where owner='%s' group by owner,object_type" %(tab_schema.upper())
ora_query_detail = "select upper(owner),upper(table_name) from dba_tables where owner='%s' order by owner,table_name fetch first 10 rows only" %(tab_schema.upper())

#select_ora_data_to_file( DynSql=ora_query_sum, FileName="ora_tab.txt")
#select_ora_data_to_file( DynSql=ora_query_detail, FileName="ora_tab.txt")


ora_query_ddl = "select dbms_metadata.get_ddl('TABLE','T_CLOB','TEST') from dual" 
select_ora_lobdata_to_file( DynSql=ora_query_detail, FileName="ora_get_ddl.txt")

'''
-----
ora_query_ddl = "select dbms_metadata.get_ddl('TABLE','%s','%s') from dual" %(tab_name.upper(), tab_schema.upper())
ora_query_ddl = "select dbms_metadata.get_ddl('TABLE','T_CLOB','TEST') from dual" 

select dbms_metadata.get_ddl('TABLE','IDT_27023','TS_COMS') from dual
select dbms_metadata.get_ddl('TABLE','T_CLOB','TEST') from dual

cnx = cx_Oracle.connect(user="ljsuser",
        password="ljspassword",
        dsn="172.16.4.87:1521/oratidb")

cnx = cx_Oracle.connect(user="ljs_20211207",
        password="ljs_20211207",
        dsn="172.16.4.87:1521/gbk")
cursor1 = cnx.cursor()
cursor1.execute(ora_query_sum)

cursor2 = cnx.cursor()
cursor2.execute(ora_query_detail)

cursor3 = cnx.cursor()
cursor3.execute(ora_query_ddl)
'''

