
##DDL files

#mysql
mysqldump -h172.16.5.103 -P5003 --skip-lock-tables -uroot -d coms > QA.coms.ddl
mysqldump -h172.16.5.103 -P5003 --skip-lock-tables -uroot -t coms > QA.coms.dml

mysql -h172.16.4.81 -P4100 -uabcuser1 -p123456  ts_coms < QA.coms.ddl

#oracle
exp ts_coms/ts_coms@gbk file=ts_coms.tabs.dmp rows=n owner=ts_coms 

imp ts_coms/ts_coms@oratidb file=ts_coms.tabs.dmp
