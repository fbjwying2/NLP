# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os


def fwrite_link(path, item):
    news_file_path = path + "/foshannews_link.txt"
    with open(news_file_path, 'a') as fw:
        fw.write("{}\n".format(item['contents']['link']))

class NewsPipeline(object):

    def process_item(self, item, spider):
        dir_path = 'output'

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        news_file_path = dir_path + "/foshannews.txt"
        with open(news_file_path, 'a') as fw:
            docs = item['contents']['title'].strip().strip('　　') + '\n'
            ttt = item['contents']['passage']
            for tt in ttt:
                docs += tt.strip().strip('　　') + '\n'

            fw.write("{}".format(docs))

        fwrite_link(dir_path, item)

        return item

