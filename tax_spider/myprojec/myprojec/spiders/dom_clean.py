from bs4 import BeautifulSoup
import re


def bs_parse(dom, spider_name):
    a = "".join(dom)
    soup = BeautifulSoup(a, "html5lib")
    tags = soup.find_all(re.compile("\w*"))
    for tag in tags:
        nms = tuple(tag.attrs.keys())
        for nm in nms:
            if nm == "src":
                src_first = tag["src"]
                if spider_name == "chinatax":
                    src_temp = src_first[8:]
                    src_value = "http://www.chinatax.gov.cn" + src_temp
                elif spider_name == "taxqi":
                    src_value = "http://www.taxqi.com" + src_first
                elif spider_name == "zjds":
                    src_value = src_first
                elif spider_name == "temp":
                    src_value = src_first
                tag["src"] = src_value
            else:
                del tag[nm]
    try:
        b = list(soup.body.contents)
    except Exception as e:
        print(e)
    bs_result = ''
    for cc in b:
        bs_result += str(cc)
    return bs_result

