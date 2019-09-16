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
        item['peops'] = response.xpath('//span[@class="s_r"]/text()').extract()
        item['salary'] = response.xpath('//p[@class="jp"]/text()').extract()
        item['experience'] = response.xpath('//span[@class="s_n"]/text()').extract()
        item['education'] = response.xpath('//span[@class="s_x"]/text()').extract()
        item['company'] = response.xpath('//*[@id="pageContent"]/div[2]/a[1]/p/text()').extract()
        item['com_info'] = response.xpath('//*[@id="pageContent"]/div[2]/a[1]/div/text()').extract()
        item['job_info'] = response.xpath('//div[@class="ain"]/article//text()').extract()
        # job_info = soup.select('.ain')[0].text()
        # print(item['company'])
        # print(item['job_info'])
        # item['job_info'] = list(''.join(job_info).replace("\n","").replace("\t","").replace("\xa0","").replace("\r",""))
        # print(item['job_info'])
        return item
