# -*- coding: utf-8 -*-
import scrapy


class UserSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass
