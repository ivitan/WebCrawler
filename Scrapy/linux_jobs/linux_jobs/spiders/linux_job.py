# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from linux_jobs.items import LinuxJobsItem


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
        item['name'] = response.xpath('//div[@class="jt"]/p/text()').extract()
        item['city'] = response.xpath('//div[@class="jt"]/em/text()').extract()
        item['salary'] = response.xpath('//p[@class="jp"]/text()').extract()
        item['experience'] = response.xpath('//*[@id="pageContent"]/div[1]/div[2]/span[2]/text()').extract()
        item['education'] = response.xpath('//*[@id="pageContent"]/div[1]/div[2]/span[3]/text()').extract()
        item['company'] = response.xpath('//*[@id="pageContent"]/div[2]/a[1]/p/text()').extract()
        item['com_info'] = response.xpath('//*[@id="pageContent"]/div[2]/a[1]/div/text()').extract()
        item['job_info'] = response.xpath('//*[@id="pageContent"]/div[3]/div[3]/article//text()').extract()
        return(item)
