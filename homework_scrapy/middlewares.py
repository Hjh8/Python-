# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import requests
from lxml import etree


class UserAgentDownloadMiddle(object):
    # 设置反爬虫-请求头
    UserAgent = ['http://www.useragentstring.com/index.php?id=19919',
                 'http://www.useragentstring.com/index.php?id=17114',
                 'http://www.useragentstring.com/index.php?id=19942',
                 'http://www.useragentstring.com/index.php?id=16275',
                 'http://www.useragentstring.com/index.php?id=13672']

    def process_request(self,request,spider):
        us = random.choice(self.UserAgent)
        request.headers['User-Agent'] = us


class IPProxyDownloadMiddle(object):
    # 设置反爬虫-IP地址 (因为免费代理不稳定，所以这里只实现代码，在settings中没有打开此中间件)
    Proxy_url = "https://www.kuaidaili.com/free/inha/1/"
    PROXY = []  # 存放爬取到的IP地址
    pro = ""  # 链接IP跟端口号

    def process_request(self,request,spider):
        self.get_proxy(spider=spider)
        proxy = random.choice(self.PROXY)  # 随机选一个IP地址
        request.meta['proxy'] = proxy

    def get_proxy(self,spider):
        # 单独爬取代理网的数据，来提取IP代理
        response = requests.get(self.Proxy_url)
        text = response.text
        html = etree.HTML(text, etree.HTMLParser())
        trs = html.xpath("//table[@class='table table-bordered table-striped']//tr")[1:]
        for tr in trs:
            IP = tr.xpath("./td[@data-title='IP']/text()")
            PORT = tr.xpath("./td[@data-title='PORT']/text()")
            pro = "HTTP://"+"".join(IP)+":"+"".join(PORT)
            self.PROXY.append(pro)

