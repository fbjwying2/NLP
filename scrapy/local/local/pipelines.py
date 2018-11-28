# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os


def fwrite_link(path, item):
    news_file_path = path + "/foshanlocal_link.txt"
    with open(news_file_path, 'a') as fw:
        fw.write("{}\n".format(item['link']))
        
        
def fwrite_name(path, item):
    news_file_path = path + "/foshanlocal_name.txt"
    with open(news_file_path, 'a') as fw:
        fw.write("{}\n".format(item['title']))
        if item['has_child']:
            for c in item['child_info']['title']:
                fw.write("{}\n".format(c))

        if item['has_community']:
            for c in item['community']['street']:
                c = c.strip().split(' ')
                fw.write("{}\n".format(c[2]))

class NewsPipeline(object):

    def process_item(self, item, spider):
        dir_path = 'output'

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        news_file_path = dir_path + "/foshanlocal.txt"
        with open(news_file_path, 'a') as fw:
            docs = ""
            sentenses = item['contents']
            for sentense in sentenses:
                docs += sentense.strip().strip(' ') + '\n'

            fw.write("{}".format(docs))

        fwrite_link(dir_path, item)

        fwrite_name(dir_path, item)

        return item