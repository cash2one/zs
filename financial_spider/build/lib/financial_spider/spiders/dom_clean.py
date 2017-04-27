from bs4 import BeautifulSoup
import re


def bs_parse(dom):
    a = "".join(dom)
    soup = BeautifulSoup(a, "html5lib")
    tags = soup.find_all(re.compile("\w*"))
    for tag in tags:
        nms = tuple(tag.attrs.keys())
        for nm in nms:
            if nm == "src":
                pass
            else:
                del tag[nm]
    try:
        b = list(soup.body.contents)
    except Exception as e:
        # print('111111', soup.body, soup)
        print(e)
    bs_result = ''
    for cc in b:
        bs_result += str(cc)
    return bs_result

