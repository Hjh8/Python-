# -*- coding: utf-8 -*-
from collections import Counter
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from homework_scrapy.items import HomeworkScrapyItem
import re
import jieba


class WxjcSpider(CrawlSpider):
    name = 'wxjc'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        # 指定爬取每一页网址的规则
        Rule(LinkExtractor(allow=r'.+\?mod=list&catid=2&page=\d+'), follow=True),
        # 指定爬取每一个文章具体内容网址的规则
        Rule(LinkExtractor(allow=r'.+article.+\.html'), callback="parse_detail" ,follow=False),
    )

    def parse_detail(self, response):
        word_c = Counter() # 用来获取词频
        word = [] # 存放词频高的词

        title = response.xpath("//div[@class='cl']/h1/text()").get().strip()  # 获取标题
        p_biaoqian = response.xpath("//div[@class='cl']/p")  # 获取p标签
        author = p_biaoqian.xpath("./a/text()").get()  # 获取p标签下的作者名字
        time = p_biaoqian.xpath("./span/text()").get()  # 获取p标签下发布时间
        author_img = response.xpath("//div[@class='avatar_left cl']/a/img/@src").get()  # 获取作者的头像地址
        viewnum = response.xpath("//div[@class='focus_num cl']/a/text()").get()  # 获取文章浏览量
        introduction = response.xpath("//div[@class='blockquote']/p/text()").get()  # 获取简介

        # 获取内容并去掉空白字符
        content = response.xpath("//table[@class='vwtb']//tr/td[@id='article_content']//text()").getall()
        content = re.sub(r'[\s ]*','',"".join(content))

        jbs = jieba.cut(introduction)  # 对内容进行分词
        for jb in jbs:  # 对分好的词进行分组并统计出现次数
            if len(jb)>1:
                word_c[jb] += 1
        for (k,v) in word_c.most_common(3):  # 获取出现频率最高前三个词
            word.append(k + str(v))

        # 传入Item
        item = HomeworkScrapyItem(title=title,word1=word[0],word2=word[1],word3=word[2],
                                  author=author,time=time,author_img=author_img,
                                  viewnum=viewnum,introduction=introduction,content=content)
        yield item
