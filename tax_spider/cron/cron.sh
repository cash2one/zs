#!/bin/bash

export PATH=$PATH:/usr/local/bin/
#cd /Users/xiaxiaodong/python/python3/tax_spider/myprojec/myprojec/spiders

cd $7
cd myprojec/




#nohup scrapy crawl zjds >> zjds.log 2>&1 &
export $1 $2 $3 $4 $5 $6
scrapy crawl chinatax


##!/usr/bin/python
#*/1 * * * * sh /Users/xiaxiaodong/python/python3/tax_spider/myprojec/myprojec/spiders/cron.sh
