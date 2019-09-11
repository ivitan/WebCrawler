# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class LinuxJobsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    city = Field()
    experience = Field()
    education = Field()
    recruit = Field()
    job_info = Field()
    company = Field()
    com_nature = Field()
    com_size = Field()
    com_field = Field()
