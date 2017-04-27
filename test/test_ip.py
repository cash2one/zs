# def test_ip():
#     logger = logging.getLogger("ip_poll")
#     badNum = 0
#     goodNum = 0
#     ip_first_set = RedisOpera.smembers("ip_first")
#     for proxy in ip_first_set:
#         proxy_host = "http://" + proxy.decode("utf-8")
#         proxyDict = {"http": proxy_host}
#         try:
#             response = requests.get("http://ip.chinaz.com/getip.aspx", proxies=proxyDict, timeout=5)
#             if response.status_code != 200:
#                 RedisOpera.srem("ip_first", proxy)
#                 badNum += 1
#             else:
#                 RedisOpera.smove("ip_first", "ip_pool", proxy)
#                 goodNum += 1
#                 print("get a good")
#                 print(response.content.decode("utf-8"))
#         except Exception as e:
#             print(e)
#             RedisOpera.srem("ip_first", proxy)
#             badNum += 1
#             print("it is a bad")
#     logger.info("we delete %s badnum" % badNum)
#     logger.info("we get %s goodnum" % goodNum)


def test_ip():
    ip_pool_set = RedisOpera.smembers("ip_pool")
    for proxy in ip_pool_set:
        proxy_host = "http://" + proxy.decode("utf-8")
        proxyDict = {"http": proxy_host}
        try:
            response = requests.get("http://ip.chinaz.com/getip.aspx", proxies=proxyDict, timeout=5)
            if response.status_code != 200:
                RedisOpera.srem("ip_pool", proxy)
        except Exception as e:
            print(e)
            RedisOpera.srem("ip_pool", proxy)