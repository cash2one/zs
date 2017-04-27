import requests
url = 'http://192.168.1.123:5888/update_spider'
proxy = requests.get(url, auth=("zs5scom", "zs5scom")).text
print(proxy)