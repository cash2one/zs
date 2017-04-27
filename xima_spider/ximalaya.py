# -*- coding: utf-8 -*-
import requests
import json
from lxml import html
import os

def log(*args):
    print(*args)


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
    print(type(spider.sound_id))
    return spider


def url_get(spider):
    sid = spider.sound_id
    print('sid是', sid)
    for i in sid:
        sound_url = 'http://www.ximalaya.com/tracks/' + str(i) + '.json'
    r = requests.get(sound_url)
    all_text = r.text
    key_dict = json.loads(all_text)
    spider.key_url = key_dict["play_path_64"]
    return spider


def new_directory():
    a = r'ximalaya/'
    if not os.path.exists(a):
        os.makedirs(a)


def dowmload(url, name):
    l = requests.get(url)
    name1 = r'ximalaya/'
    for i in name:
        name2 = name1 + str(i) + '.m4a'
        with open(name2, 'wb') as f:
            f.write(l.content)


def save(spider):
    try:
        name = spider.name
        url = spider.key_url
        dowmload(url, name)
        return True
    except Exception as e:
        print('Error happen: %s' % e)
        return False


def main(url):
    log('开始爬取...')
    a = analyze_url(url)
    log('analyze')
    spider = url_get(a)
    log('spider')
    new_directory()
    log('new_directory')
    if save(spider):
        log('爬取完成')
        return True
    else:
        return False

if __name__ == '__main__':
    main()

