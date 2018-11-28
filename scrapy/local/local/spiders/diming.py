
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from local.items import NewsItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import requests
import re
import json

import scrapy

# 回归测试需要验证
# https://www.foshannews.net/jdyw/201810/t20181031_202106.html
# https://www.foshannews.net/kjzt2016/gdddh_26312/02016/201811/t20181106_203505.html
# https://www.foshannews.com/kjzt2016/gdddh_26312/02016/201811/t20181105_203179.html
# https://www.foshannews.net/jdyw/201811/t20181106_203382.html
# https://www.foshannews.net/jdyw/201810/t20181031_202109.html
# https://www.foshannews.net/jdyw/201811/t20181105_203219.html

class DimingSpider(CrawlSpider):
    name = "diming"
    allowed_domains = ["cn56.net.cn"]
    start_urls = [
        'http://www.cn56.net.cn/diming/dmcxix7by2.html',
    ]

    url_pattern = r'./dm*.html'

    rules = (
        Rule(LinkExtractor(allow=(url_pattern)), 'parse'),
    )

    url_map = dict()
    def get_url_id(self, url):
        return url.split('/')[-1].split('.')[0]

    def parse(self, response):

        item = self.parse_base(response)
        yield item

        if item['has_child']:
            map_item_child = item['child_info']
            list_child_name = map_item_child['title']
            list_child_url = map_item_child['url']
            for (child_name, child_url) in zip(list_child_name ,list_child_url):
                yield scrapy.Request(url=child_url,callback=self.parse)

    def parse_base(self, response):
        item = NewsItem()
        item['link'] = str(response.url)
        item['title'] = response.xpath('//*[@id="page_left"]/h1/text()').extract_first()

        print("new itme title", item['title'])

        list_doc = []
        parent_text = response.xpath("//*[@id='page_left']/div[@class='dmcon']/text()").extract()
        for txt in parent_text:
            t = txt.strip()
            if len(t) > 0:
                list_doc.append(t)

        item['contents'] = list_doc


        _info_tree = response.xpath("//*[@id='page_left']/div[@class='infotree']")
        # xpath 判断节点是否存在
        item['has_child'] = len(_info_tree)
        if len(_info_tree):
            list_child_name = []
            list_child_url = []
            # 通过某节点作为根节点进行大类链接遍历
            for index, each in enumerate(_info_tree.xpath("./table[1]/tr")):
                # 获取大类链接和大类标题
                # encode('utf-8') string编码为bytes
                if index > 0:
                    child = each.xpath('./td[1]/strong/a')
                    child_name = child.xpath('./text()').extract_first()
                    child_url = 'http://www.cn56.net.cn/diming/' + child.xpath('./@href').extract_first()

                    list_child_name.append(child_name)
                    list_child_url.append(child_url)

            item['child_info'] = {'title': list_child_name, 'url': list_child_url}

        # page_left > div.w748 > div.w372
        _community_node = response.xpath("//*[@id='page_left']/div[@class='w748']/div[@class='w372']")
        item['has_community'] = len(_community_node)
        if len(_community_node):
            # '//*[@id="page_left"]/div[6]/div[1]/div[1]/strong'
            # page_left > div.w748 > div.w372 > div.ht
            _community_title = _community_node.xpath("./div[@class='ht']/strong/text()").extract_first()
            _list_community_text = []

            # page_left > div.w748 > div.w372 > div.f12
            parent_text = _community_node.xpath("./div[@class='f12']/text()").extract()
            for txt in parent_text:
                t = txt.strip()
                if len(t) > 0:
                    _list_community_text.append(t)

            item['community'] = {"title": _community_title, "street":_list_community_text}


        print("111111 end")

        return item


