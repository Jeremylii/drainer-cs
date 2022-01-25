#!/bin/bash
#

function f_run_findpt
{
echo ""
echo "****start  f_run_findpt  `date +%Y%m%d.%H%M%S`****"
find_count=0
find_count=`ps -ef | grep ftdb.jar | grep -v grep| wc -l`

if [ ${find_count} -gt 0 ]
then
  echo "ftdb.jar  is running, quit!!!  `date +%Y%m%d.%H%M%S`****"
  ps -ef | grep ftdb.jar
  echo ""
  return
fi

date
echo "java -Dfile.encoding=utf-8 -jar /data1/tmp/findpt_master/bin/ftdb.jar test 1005 2 RR --spring.config.location = /data1/tmp/findpt_master/bin/application.properties"
java -Dfile.encoding=utf-8 -jar /data1/tmp/findpt_master/bin/ftdb.jar test 1006 2 RR --spring.config.location = ./application.properties
date
echo "****finish f_run_findpt  `date +%Y%m%d.%H%M%S`****"
}

function f_check_drainer
{
echo "****start  check drainer  `date +%Y%m%d.%H%M%S`****"
mysql -h172.16.4.81 -P4100 -ufindpt -pfindpt -NBe 'show drainer status'
ps -ef | grep drainer
date
}

function f_restart_drainer
{
echo ""
}

function f_check_o2t
{
echo "****start  check f_check_o2t  `date +%Y%m%d.%H%M%S`****"
check_hour=`date +%M`
[ ${check_hour} -gt 5 ] && return
echo "/data1/tmp/localdrainer/oracle/o2t_sync_diff -config /data1/tmp/localdrainer/oracle/sync_ora1.toml"
/data1/tmp/localdrainer/oracle/o2t_sync_diff -config /data1/tmp/localdrainer/oracle/sync_ora1.toml
sleep 60
}

function f_main_run
{
i=0
while :
do
  echo "****start  check f_main_run $i  `date +%Y%m%d.%H%M%S`****"
  #f_check_o2t
  f_run_findpt
  f_check_drainer
  sleep 300
  i=$((i+1))
  
done
}

###################################################################################
#=========================================================================
## Begin From Here
ShellName="$(echo $0|awk -F / '{print $NF}')";
WorkDir="$(echo $0|sed s/${ShellName}//g)";[ -z "${WorkDir}" ] && WorkDir=${PWD};cd ${WorkDir};WorkDir=${PWD}
LogDir="${WorkDir}/findptlogs";mkdir -p ${LogDir};chmod -R 777 ${LogDir} 2>/dev/null
LogFile="${LogDir}/${ShellName}.log.$(date +"%Y%m%d_%H%M%S")"
source ~/.bash_profile
#=========================================================================


f_main_run >> ${LogFile}
