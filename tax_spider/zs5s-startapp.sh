#!/bin/bash


if [ $# -ne 0 ]
then
    if [[ $1 =~ ^ES_URL= ]] ; then :
    else
    echo "ES_URL is wrong" ; return -1
    fi

    if [[ $2 =~ ^ES_INDEX= ]] ; then :
    else
    echo "ES_INDEX is wrong" ; return -1
    fi

    if [[ $3 =~ ^ES_TYPE= ]] ; then :
    else
    echo "ES_TYPE is wrong" ; return -1
    fi

    if [[ $4 =~ ^REDIS_HOST= ]] ; then :
    else
    echo "REDIS_HOST is wrong" ; return -1
    fi

    if [[ $5 =~ ^REDIS_PORT= ]] ; then :
    else
    echo "REDIS_PORT is wrong" ; return -1
    fi

    if [[ $6 =~ ^LOG_PATH= ]] ; then :
    else
    echo "LOG_PATH is wrong" ; return -1
    fi
fi


echo 1

echo "#!/usr/bin/python" > cron/start_spider.sh
a=`pwd`
echo "0 0 * * * source $a/cron/cron.sh $1 $2 $3 $4 $5 $6 $a" >> cron/start_spider.sh

crontab cron/start_spider.sh
