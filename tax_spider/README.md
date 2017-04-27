# 税务爬虫(http://www.chinatax.gov.cn/)
### 功能说明：
1.爬取国家税务总局的税务相关信息
2.每天00:00增量爬取一次数据
### 环境变量说明
|环境变量名    |说明    |类型    |示例    
| :----:  | :----:  | :----:  | :----:  |
|REDIS_PORT    |redis的端口    |int|   6379  |
|REDIS_HOST    |redis的地址    |string|    dev.tax.redis.zs    |
|LOG_PATH    |logfile的路径    |string|    /Users/tax/    |
|ES_TYPE    |Elasticsearch的type    |string|    spider    |
|ES_INDEX    |Elasticsearch的index    |string|    information    |
|ES_URL     |Elasticsearch的存储地址    |string|    http://dev.tax.elasticsearch.zs    |
### 备注
启动文件地址：tax_spider/zs5s-startapp.sh
启动文件示例：source zs5s-startapp.sh ES_URL="xxx" ES_INDEX=“xxx” ES_TYPE=“xxx” REDIS_HOST=“xxx” REDIS_PORT=0000 LOG_PATH=“xxx”
