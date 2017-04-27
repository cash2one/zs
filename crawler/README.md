# 简要说明: 获取下载地址

- 接口地址：/api/v1/sound
- 请求方式：POST
- 接口格式：{"url": url}
- 响应格式：'{"key": "success", "please_copy": url}" or "{"key": "failure", "please_copy": None}'
- 返回示例: {"key": "success", "please_copy": 192.168.1.191:8000/api/v1/download/Happy Wonder World.m4a}
- 备注: 复制"please_copy"的url到浏览器即可下载

# 简要说明: 下载
- 接口地址：/api/v1/download/filename
- 请求方式：GET
- 接口格式：/api/v1/download/filename
- 请求示例: 192.168.1.191:8000/api/v1/download/Happy Wonder World.m4a



# TODO

1. 如果文件过大，同步等待下载完成的话，请求会超时， 这个问题需要考虑下怎么解决比较合适；
2.