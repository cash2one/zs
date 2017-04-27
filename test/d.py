import requests

#update_spider
# url = 'http://192.168.1.123:5999/update_spider/zs5scom'
# proxy = requests.get(url).text
# print(proxy)


#get_proxy_ip
# url = 'http://192.168.1.123:5999/'
# proxy = requests.get(url, auth=("zs5scom", "zs5scom")).text
# print(proxy)


#change_time
# url = 'http://192.168.1.123:5999/change/spider_time/<time_int>'
# proxy = requests.get(url, auth=("zs5scom", "zs5scom")).text
# print(proxy)


#change_scrapyd_url
url = 'http://192.168.1.192:5999/change/scrapyd_url/localhadfost:6800'
proxy = requests.get(url, auth=("zs5scom", "zs5scom")).text
print(proxy)




# 125.109.192.98:3128
# str = '''<P>上海莲露美容美发有限公司：</P>
# <P>　　本会已受理申请人汪合云与你单位的劳动争议案（案号：静劳人仲(2016)办字第2320号），现已审理终结。申请人汪合云在收到本会发出的开庭通知后无正当理由拒不到庭，根据《中华人民共和国劳动争议调解仲裁法》之有关规定，本会对静劳人仲(2016)办字第2320号案件按撤回仲裁申请处理。因你单位未按规定参加仲裁活动且公司负责人下落不明，依照《劳动人事争议仲裁办案规则》规定向你单位公告送达通知。</P>
# <P>　　自公告发布之日起，经过六十日，即视为送达。</P>
# <P>　　特此公告</P>
# <P align=right>　　<BR>二○一七年三月三日<BR></P> '''
# print(str)

# def a(b):
#     for i in b:
#         print("123")
#         yield i
#         print("666")
#     return "777"
# b = [1,2,3]
# print(a(b))