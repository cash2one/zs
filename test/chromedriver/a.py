#coding:utf-8
from selenium import webdriver

import time

dr = webdriver.Chrome('/Users/xiaxiaodong/tool/chromedriver')


print('Browser will be closed')

dr.quit()

print('Browser is close')