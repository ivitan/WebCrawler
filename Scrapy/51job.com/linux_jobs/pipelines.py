# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os


class Pipeline_ToCSV(object):

    def __init__(self):
        self.csvwriter = csv.writer(open('jobs.csv', 'w'), delimiter=',')
        self.csvwriter.writerow(['name','city','peops','experience','salary','education','company','com_info','jpb_info'])

    def process_item(self, item, ampa):
        rows = zip(item['name'],item['city'],item['peops'],item['experience'],item['salary'],item['education'],item['company'],item['com_info'],item['job_info'])

        for row in rows:
            self.csvwriter.writerow(row)

        return item