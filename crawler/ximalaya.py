# encoding: utf-8
import requests
import json
from lxml import html
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def log(*args):
    print(args)


class Spiderman(object):
    def __init__(self):
        self.name = ''
        self.sound_id = ''
        self.key_url = ''


spider = Spiderman()


def analyze_url(url):
    r = requests.get(url)
    temp = html.fromstring(r.content)
    spider.name = temp.xpath('//div[@class="detailContent_title"]/h1/text()')
    if url.find('sound') != -1:
        a = []
        b = str(url.split('sound/')[-1])
        a.append(b)
        spider.sound_id = a
    else:
        spider.sound_id = temp.xpath('//div[@class="detailContent"]/@sound_id')
    return spider


def url_get(spider):
    sid = spider.sound_id
    for i in sid:
        sound_url = 'http://www.ximalaya.com/tracks/' + str(i) + '.json'
    r = requests.get(sound_url)
    all_text = r.text
    key_dict = json.loads(all_text)
    spider.key_url = key_dict["play_path_64"]
    return spider


def dowmload(url, name, download_dir):
    l = requests.get(url)
    for i in name:
        basename = str(i) + '.m4a'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        with open(os.path.join(download_dir, basename), 'wb') as f:
            f.write(l.content)


def save(spider, download_dir):
    try:
        name = spider.name
        url = spider.key_url
        dowmload(url, name, download_dir)
        return True
    except Exception as e:
        return False


def main(url, download_dir='ximalaya_downloads'):
    a = analyze_url(url)
    spider = url_get(a)
    if save(spider, download_dir):
        name = spider.name
        return name
    else:
        return False


if __name__ == '__main__':
    main()
