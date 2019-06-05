#!/bin/bash
#GRANT SELECT, RELOAD, LOCK TABLES, REPLICATION CLIENT, SHOW VIEW, TRIGGER ON *.* TO 'xxx'@'127.0.0.1' identified by "xxx";
#grant SELECT, RELOAD, LOCK TABLES, SHOW VIEW, TRIGGER on *.* to 'xxx'@'127.0.0.1' identified by "xxx";
DATE=$(date +%Y%m%d)
BAKPATH=/data/bak
BAKLOG=${BAKPATH}/baklog
MYUSER=xxx
MYPASS=xxx
MYCMD="/data/app/mysql/bin/mysql -u${MYUSER} -p$MYPASS -h 127.0.0.1 -P 3660"
MYDUMP="/data/app/mysql/bin/mysqldump -u${MYUSER} -p$MYPASS -h 127.0.0.1 -P 3660 -R -F --single-transaction -B"
DBLIST=`${MYCMD} -e "show databases;" | sed 1d | egrep -v "_schema|mysql|sys|test|zabbix"`
IP=192.168.2.11
W=/bak
lastfilesize=`curl -H "Content-Type: application/json" -X POST  --data '{"last_filesize":"l"}'  http://192.168.100.254:5000/mrecord`

pre(){
 MC=`mount|grep bak|wc -l`
# [ ! ${MC} -eq 1 ]&& mount -t cifs -o credentials=/root/x.txt,sec=ntlm //192.168.2.1/mysql ${W}
 #create backup directory
 [ ! -d ${BAKPATH} ] && mkdir -p ${BAKPATH}
 [ ! -d ${BAKLOG} ] && mkdir -p ${BAKLOG}
}
bak(){
 for dbname in ${DBLIST}
 do
   bakpath=${BAKPATH}/${dbname}
   [ ! -d ${bakpath} ]&&mkdir -p ${bakpath}
   BAKNAME="${IP}"_${dbname}_"${DATE}".sql.gz
   starttime=$(date +%s)
   ${MYDUMP} ${dbname} | gzip > ${BAKPATH}/${dbname}/"${IP}"_${dbname}_"${DATE}".sql.gz
   stoptime=$(date +%s)
   costtime=`expr ${stoptime} - ${starttime}`
   md5=`md5sum ${BAKPATH}/${dbname}/"${IP}"_${dbname}_"${DATE}".sql.gz|awk '{print $1}'`
   rsync -rltpDPvz ${BAKPATH}/${dbname}/"${IP}"_${dbname}_"${DATE}".sql.gz ${W}
   [ $? -eq 0 ]&&to_f01=1||to_f01=0
   filesize=`du -b ${bakpath}/${BAKNAME}|awk '{print $1}'`
   incsize=`expr ${filesize} - ${lastfilesize}`
   data=\{\"ip\":\"${IP}\",\"bakname\":\"${BAKNAME}\",\"bakdir\":\"${bakpath}\",\"md5sum\":\"${md5}\",\"filesize\":\"${filesize}\",\"starttime\":\"${starttime}\",\"stoptime\":\"${stoptime}\",\"costtime\":\"${costtime}\",\"incsize\":\"${incsize}\",\"to_f01\":\"${to_f01}\",\"mark\":\"fortest\"\}
   curl -H "Content-Type: application/json" -X POST  --data ${data}  http://192.168.100.254:5000/mrecord
 done
}
after(){
 #local save data for 30 days
 find ${BAKPATH} -type f -name "*sql*" -mtime +30 | xargs rm -f
}

pre
bak
after
