import requests


#get_proxy_ip
url = 'http://127.0.0.1:5999'
proxy = requests.get(url, auth=("zs5scom", "zs5scom")).text
print(proxy)
