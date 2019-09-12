# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from linux_jobs.items import LinuxJobsItem


class LinuxJobSpider(Spider):
    name = 'linux_job'
    allowed_domains = ['51job.com']
    start_urls = [
        'https://search.51job.com/list/000000,000000,0000,00,9,99,linux,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=4&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    def parse(self, response):
        # 获取一页的URL
        url_lis = response.xpath('//div[@class="el"]/p/span/a/@href').extract()

        # 调用函数获取信息
        for url in url_lis:
            yield Request(url, callback=self.parse_detail)

        # # 下一页
        # next_page = response.xpath('//div[@class="p_in"]/ul/li[last()]/a/@href').extract()
        #
        # if next_page:
        #     next_page = response.urljoin(next_page[0])
        #     yield Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = LinuxJobsItem()
        item['name'] = response.xpath('//div[@class="cn"]/h1/text()').extract()
        item['city'] = response.xpath('//div[@class="cn"]/p[2]/text()').extract()[0].split()
        item['experience'] = response.xpath('//div[@class="cn"]/p[2]/text()').extract()[1].split()
        item['salary'] = response.xpath('//div[@class="cn"]/strong/text()').extract()
        item['education'] = response.xpath('//div[@class="cn"]/p[2]/text()').extract()[2].split()
        item['company'] = response.xpath('//div[@class="com_msg"]/a/p/text()').extract()
        item['com_nature'] = response.xpath('//div[@class="com_tag"]/p[1]/text()').extract()
        item['com_size'] = response.xpath('//div[@class="com_tag"]/p[2]/text()').extract()
        item['com_field'] = response.xpath('//div[@class="com_tag"]/p[3]/a/text()').extract()
        item['job_info'] = ''.join(response.xpath('//div[@class="bmsg job_msg inbox"]//text()').extract())
        print(item)
        return item
