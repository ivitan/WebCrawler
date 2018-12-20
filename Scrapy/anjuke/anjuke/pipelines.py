# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os


class Pipeline_ToCSV(object):

    def __init__(self):
        self.csvwriter = csv.writer(open('anjuke.csv', 'w'), delimiter=',')
        self.csvwriter.writerow(['date','tittle', 'price', 'huxing', 'area','built','chaoxiang','leibie','loucheng','zhuangxiu'])

    def process_item(self, item, ampa):
        rows = zip(item['date'],item['tittle'], item['price'],item['huxing'],item['area'],item['built'],item['chaoxiang'],item['leixing'],item['louceng'],item['zhuangxiu'])

        for row in rows:
            self.csvwriter.writerow(row)

        return item
