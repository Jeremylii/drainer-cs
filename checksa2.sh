#!/bin/bash

function f_check
{
i=0
customer_count=0
echo ""
date
echo "****start check customer count ****"
echo "connect info -hxxx.xx.xx.xx -P5000"
while [ $i -lt 500 -a $customer_count -lt 1000000 ]
do 
  customer_count=`mysql -hxxx.xx.xx.xx -P5000 -uabcuser1 -pxxxxx -NBe 'select count(1) from findpt.customer'`
  echo "table customer row count: $customer_count and now is `date +%Y%m%d.%H%M%S` , the $i loop"
  i=$((i+1))
  sleep 10
done
echo "****finish check customer count ****"

i=0
account_count=0
echo ""
date
echo "****start check account count ****"
echo "connect info -hxxx.xx.xx.xx -P5000"
while [ $i -lt 1000 -a $account_count -lt 10000000 ]
do 
  account_count=`mysql -hxxx.xx.xx.xx -P5000 -uabcuser1 -pxxxxx -NBe 'select count(1) from findpt.account'`
  echo "table account row count: $account_count and now is `date +%Y%m%d.%H%M%S` , the $i loop"
  i=$((i+1))
  sleep 30
done
echo "****finish check account count ****"
}

function f_check_truncate
{
i=0
customer_count=99
echo ""
date
echo "****start check customer count ****"
echo "connect info -hxxx.xx.xx.xx -P5000"
while [ $i -lt 1000 -a $customer_count -gt 10 ]
do
  customer_count=`mysql -hxxx.xx.xx.xx -P5000 -uabcuser1 -pxxxxx -NBe 'select count(1) from findpt.branch'`
  echo "table branch row count: $customer_count and now is `date +%Y%m%d.%H%M%S` , the $i loop"
  i=$((i+1))
  sleep 2
done
echo "****finish check customer count ****"

i=0
account_count=99
echo ""
date
echo "****start check account count ****"
echo "connect info -hxxx.xx.xx.xx -P5000"
while [ $i -lt 100 -a $account_count -gt 10 ]
do
  account_count=`mysql -hxxx.xx.xx.xx -P5000 -uabcuser1 -pxxxxx -NBe 'select count(1) from findpt.account'`
  echo "table account row count: $account_count and now is `date +%Y%m%d.%H%M%S` , the $i loop"
  i=$((i+1))
  sleep 5
done
echo "****finish check account count ****"
}

###################################################################################
#=========================================================================
## Begin From Here
ShellName="$(echo $0|awk -F / '{print $NF}')";
WorkDir="$(echo $0|sed s/${ShellName}//g)";[ -z "${WorkDir}" ] && WorkDir=${PWD};cd ${WorkDir};WorkDir=${PWD}
LogDir="${WorkDir}/logs";mkdir -p ${LogDir};chmod -R 777 ${LogDir} 2>/dev/null
LogFile="${LogDir}/${ShellName}.log.$(date +"%Y%m%d_%H%M%S")"

#=========================================================================

f_check | tee -a ${LogFile}
f_check_truncate | tee -a ${LogFile}
