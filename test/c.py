import requests

proxies = {
  "http": "http://115.221.118.121:3128",
}

a = requests.get("http://hl.lss.gov.cn/hljszc/more.jsp?type=005.001&key1=&key2=&key3=&key4=&page=1", proxies=proxies)

print(a.content)

# import requests
# from lxml import html
#
# page = requests.get("http://hl.lss.gov.cn/hljszc/view.jsp?id=2007")
# tree = html.fromstring(page.text)
# a = tree.xpath("//td/text()")
# if a == []:
#   print(type(a))
