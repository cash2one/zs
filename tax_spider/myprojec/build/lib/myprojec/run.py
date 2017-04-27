from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import time
import os

runner = CrawlerRunner(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
d = runner.crawl('zjds')
d.addBoth(lambda _: reactor.stop())
reactor.run()
time.sleep(100)
os.system('python3 run.py')