import requests


#get_proxy_ip
url = 'http://45.63.123.116:5999'
proxy = requests.get(url, auth=("zs5scom", "zs5scom")).text
print(proxy)


#update_spider
# url = 'http://192.168.5.220:5888/update_spider'
# proxy = requests.get(url, auth=("zs5scom", "zs5scom")).text
# print(proxy)


# change_time
# url = 'http://192.168.5.220:5888/change/spider_time/900'
# proxy = requests.get(url, auth=("zs5scom", "zs5scom")).text
# print(proxy)


#change_scrapyd_url
# url = 'http://192.168.5.220:5888/change/scrapyd_url/192.168.5.220:6800'
# proxy = requests.get(url, auth=("zs5scom", "zs5scom")).text
# print(proxy)

