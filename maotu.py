#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-10-30 18:01:28
# Project: Maotu

from pyspider.libs.base_handler import *
import pymongo

class Handler(BaseHandler):
    crawl_config = {
    }
    client = pymongo.MongoClient('localhost')
    db = client['maotu']
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.tripadvisor.cn/Attractions-g294217-Activities-Hong_Kong.html', callback=self.index_page,validate_cert=False,fetch_type='js')

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.attraction_element .listing_title  > a').items():
            self.crawl(each.attr.href, callback=self.detail_page,validate_cert=False,fetch_type='js')
        nextlink = response.doc('.nav.next').attr.href
        self.crawl(nextlink,callback=self.index_page,validate_cert=False,fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
            name =  response.doc('.h1').text(),
            rank =response.doc('b > span').text(),
            location = response.doc('.headerBL > div').text(),
            view = response.doc('.seeAllReviews').text()[:-3],
            score = response.doc('.overallRating').text(),
            kfsj = response.doc('.headerBL .header_detail').text()[5:],
            phone = response.doc('.contact > .phone > div').text()[0:-4]
            return {
                "name":name,
                "rank":rank,
                "location":location,
                "view":view,
                 "score":score,
                "kf":kfsj,
                "phone":phone
        }
            
    def on_result(self,result):
                if result:
                       self.save_to_mango(result)

    def save_to_mango(self,result):
                if self.db['MaoTU_HongKong'].insert(result):
                    print('savinf to mango',result)
