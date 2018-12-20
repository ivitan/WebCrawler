# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from anjuke.items import AnjukeItem


class AnjukehouseSpider(Spider):
    name = 'anjukeHouse'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://guangzhou.anjuke.com/sale/p1-rd1/#filtersort']

    def parse(self, response):
        # 所有URL
        urlList = response.xpath('//div[contains(@class,"house-title")]/a/@href').extract()
        for url in urlList:
            yield Request(url,callback=self.parse_detail)

        # 下一页
        next = response.xpath('//*[@id="content"]/div[4]/div[7]/a[7]/@href').extract()
        if next:
            next = response.urljoin(next[0])
            yield Request(next,callback=self.parse)

    def parse_detail(self,response):
        item = AnjukeItem()
        item['date'] = response.xpath('//span[@class="house-encode"]/text()').extract()[0].split()
        item['tittle'] = response.xpath('//h3[@class="long-title"]/text()').extract()
        item['price'] = response.xpath('//span[@class="light info-tag"]/em/text()').extract_first().split()

        houseInfo = response.xpath('//div[@class="houseInfo-content"]/text()').extract()
        item['huxing'] = houseInfo[2].strip().replace("\n","").replace("\t","").split()
        item['area'] = houseInfo[7].strip().split()
        item['built'] = houseInfo[9].strip().replace("\n", "").replace("\t", "").split()
        item['chaoxiang'] = houseInfo[10].strip().split()
        item['leixing'] = houseInfo[-8].strip().split()
        item['louceng'] = houseInfo[-7].strip().split()
        item['zhuangxiu'] = houseInfo[-6].strip().split()
        print(item)
        return item

