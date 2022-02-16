# -*- coding: utf-8 -*-
#
"""
生成建表语句
"""

datatype_mapping = {
	"TINYINT":"NUMBER(3, 0)",
	"SMALLINT":"NUMBER(5, 0)",
	"MEDIUMINT":"NUMBER(7, 0)",
	"INT":"NUMBER(10, 0)",
	"INTEGER":"NUMBER(10, 0)",
	"BIGINT":"NUMBER(19, 0)",
	"FLOAT":"FLOAT",
	"DOUBLE":"FLOAT(24)",
	"DECIMAL":"FLOAT(24)",
	"REAL":"FLOAT(24)",

	"DATE":"DATE",
	"TIME":"DATE",
	"DATETIME":"DATE",
	"TIMESTAMP":"DATE",
	"YEAR":"NUMBER",

	"CHAR":"CHAR",
	"VARCHAR":"VARCHAR2",
	"BIT":"RAW",
	"TEXT":"CLOB",
	"TINYTEXT":"VARCHAR2",
	"MEDIUMTEXT":"CLOB",
	"LONGTEXT":"CLOB",

	"BINARY":"",
	"VARBINARY":"",

	"BLOB":"BLOB",
	"TINYBLOB":"RAW",
	"MEDIUMBLOB":"BLOB",
	"LONGBLOB":"BLOB",
	"ENUM":"VARCHAR2",
	"SET":"VARCHAR2"
}

datatype_length = {
	"TINYINT":"NUMBER(3, 0)",
	"SMALLINT":"NUMBER(5, 0)",
	"MEDIUMINT":"NUMBER(7, 0)",
	"INT":"NUMBER(10, 0)",
	"INTEGER":"NUMBER(10, 0)",
	"BIGINT":"NUMBER(19, 0)",
	"FLOAT":"FLOAT",
	"DOUBLE":"FLOAT(24)",
	"DECIMAL":"FLOAT(24)",
	"REAL":"FLOAT(24)",

	"DATE":"DATE",
	"TIME":"DATE",
	"DATETIME":"DATE",
	"TIMESTAMP":"DATE",
	"YEAR":"NUMBER",

	"CHAR":"255",
	"VARCHAR":"16383",
	"BIT":"RAW",
	"TEXT":"65535",
	"TINYTEXT":"255",
	"MEDIUMTEXT":"16777215",
	"LONGTEXT":"4294967295",

	"BINARY":"",
	"VARBINARY":"",

	"BLOB":"65535",
	"TINYBLOB":"255",
	"MEDIUMBLOB":"16777215",
	"LONGBLOB":"4294967295",
	"ENUM":"VARCHAR2",
	"SET":"VARCHAR2"
}


char_type_contain =  {"tabname": "TEST_CHAR1", "tabcol": ["CHAR(20)", "VARCHAR(20)", "VARCHAR(5000)", "VARCHAR(15000)", "TEXT"]}
int_type_contain =  {"tabname": "TEST_INT1", "tabcol": ["INT", "DOUBLE", "FLOAT(4)", "DECIMAL(12,1)", "INTEGER(11)"]}
date_type_contain =  {"tabname": "TEST_DATE1", "tabcol": ["DATETIME", "DATE"]}
lob_type_contain =  {"tabname": "TEST_LOB1", "tabcol": ["TEXT", "LONGTEXT", "BLOB"]}




def f_crt_tab_str(dbtype,tabinfo):
    """
    Generate create table DDL , Tidb is source
    """
    table_prefix= {"oracle":"id INT not null primary key ,\n  ts DATE ,",
               "mysql":"id INT not null primary key ,\n  ts DATETIME,",
               "tidb":"id INT not null primary key AUTO_INCREMENT,\n  ts DATETIME default now(),"
              }

    table_suffix= {"oracle": " ",
               "mysql": "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ",
               "tidb": "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin "
              }

    tab_nam = tabinfo["tabname"]
    col_lst = tabinfo["tabcol"]

    tab_prefix = table_prefix[dbtype]
    tab_suffix = table_suffix[dbtype]
    i_len = len(col_lst)
    i = 1
    print ("""create table %s \n (%s """ % (tab_nam, tab_prefix))
    for col_type in col_lst:
        if dbtype == "oracle" and "(" in col_type:
            col_type1 = col_type.split("(")[0]
            col_type2 = col_type.split("(")[1]
            if "(" in datatype_mapping[col_type1]:
                col_type = datatype_mapping[col_type1]
            else:
            	col_type = datatype_mapping[col_type1]+"("+col_type2

        if i < i_len:
        	col_str = "  col%s %s," %(i, col_type)
        else:
        	col_str = "  col%s %s" %(i, col_type)

        print (col_str)
        i = i + 1
    print (") " + tab_suffix + ";")


def f_crt_tab_exec(dbtype,tabinfo):
    """
    Exec create table DDL 
    """



#f_crt_tab_tidb(char_type_contain)
f_crt_tab_str("tidb", char_type_contain)
f_crt_tab_str("mysql", char_type_contain)
f_crt_tab_str("oracle", char_type_contain)


f_crt_tab_str("tidb", int_type_contain)
f_crt_tab_str("oracle", int_type_contain)


import cx_Oracle
dsn_tns = cx_Oracle.makedsn('172.16.4.87', '1521', service_name='gbk') 
conn = cx_Oracle.connect(user="ljs_20211207", password="ljs_20211207", dsn=dsn_tns )

c = conn.cursor()

c.execute("""
    begin
        execute immediate 'drop table TEST_INT1';
        exception when others then if sqlcode <> -942 then raise; end if;
    end;""")

c.execute("""
        create table TEST_INT1 
        (id INT not null primary key ,
        ts DATE , 
        col1 INT,
        col3 FLOAT(4),
        col4 FLOAT(24),
        col5 NUMBER(10, 0)
        );
    """)


