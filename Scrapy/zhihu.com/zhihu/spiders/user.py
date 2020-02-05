# -*- coding: utf-8 -*-
from pandas.io import json
from scrapy import Spider,Request
from zhihu.items import UserItem


class UserSpider(Spider):
    name = 'user'
    allowed_domains = ['www.zhihu.com']

    start_user = 'wang-ni-ma-94'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        # 请求开始用户
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)

        # 请求用户关注列表
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, limit=20, offset=0),self.parse_follows)

        # 请求用户粉丝列表
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=0),self.parse_followers)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()

        for field in item.fields:
            # 如果field是item键程之一就item赋值
            if field in result.keys():
                # 如果属性是之一是返回的json结果的就对他进行赋值
                item[field] = result.get(field)
        yield item

        # 对每个用户请求获取他的关注列表
        yield Request(self.follows_url.format(user=result.get('url_token'), include=self.follows_query, limit=20, offset=0),self.parse_follows)

        # 对每个用户请求获取他的粉丝列表
        yield Request( self.followers_url.format(user=result.get('url_token'), include=self.followers_query, limit=20, offset=0),self.parse_followers)

    def parse_follows(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),self.parse_user)

         # 分页判断，
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page,self.parse_follows)

    def parse_followers(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              self.parse_user)

        # 分页判断，
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page,
                          self.parse_followers)



