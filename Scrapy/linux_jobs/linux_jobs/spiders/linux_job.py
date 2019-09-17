# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from linux_jobs.items import LinuxJobsItem
from bs4 import BeautifulSoup
import re


class LinuxJobSpider(Spider):
    name = 'linux_job'
    allowed_domains = ['51job.com']
    start_urls = ['https://m.51job.com/search/joblist.php?keyword=linux&keywordtype=2']

    def parse(self, response):
        # 获取一页的URL
        url_lis = response.xpath('//div[@class="items"]/a/@href').extract()

        # 调用函数获取信息
        for url in url_lis:
            yield Request(url, callback=self.parse_detail)

        # 下一页
        next_page = response.xpath('//*[@id="turnpage"]/div/a[2]/@href').extract()

        if next_page:
            next_page = response.urljoin(next_page[0])
            yield Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = LinuxJobsItem()
        soup = BeautifulSoup(response.body,'lxml')
        item['name'] = response.xpath('//div[@class="jt"]/p/text()').extract()
        item['city'] = response.xpath('//div[@class="jt"]/em/text()').extract()

        peops = response.xpath('//span[@class="s_r"]/text()').extract()
        if peops:
            item['peops'] = peops
        else:
            item['peops'] = ['暂无信息']

        salary = response.xpath('//p[@class="jp"]/text()').extract()
        if salary:
            item['salary'] = salary
        else:
            item['salary'] = ['暂无信息']

        experience = response.xpath('//span[@class="s_n"]/text()').extract()
        if experience:
            item['experience'] = experience
        else:
            item['experience'] = ['无要求']

        education = response.xpath('//span[@class="s_x"]/text()').extract()
        if education:
            item['education'] = education
        else:
            item['education'] = ['暂无信息']

        item['company'] = response.xpath('//*[@id="pageContent"]/div[2]/a[1]/p/text()').extract()
        item['com_info'] = response.xpath('//*[@id="pageContent"]/div[2]/a[1]/div/text()').extract()
        job_info = response.xpath('//div[@class="ain"]/article//text()').extract()
        item['job_info'] = [job_info]
        return item
