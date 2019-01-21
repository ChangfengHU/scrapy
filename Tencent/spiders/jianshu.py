# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Tencent.items import ArticleItem
class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://www.jianshu.com/']
    count=0
    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.count=self.count+1
        title= response.xpath("//h1[@class='title']/text()").get()
        avatar= response.xpath("//div[@class='author']/a[@class='avatar']/img/@src").get()
        author= response.xpath("//span[@class='name']/a/text()").get()
        content= response.xpath("//div[@class='show-content']").get()
        pub_time= response.xpath("//span[@class='publish-time']/text()").get().replace("*","")
        article_id=response.url.split("?")[0].split("p/")[1]
        word_count= response.xpath("//span[@class='wordage']/text()").get()
        comment_count= response.xpath("//span[@class='comments-count']/text()").get()
        read_count= response.xpath("//span[@class='views-count']/text()").get()
        like_count= response.xpath("//span[@class='likes-count']/text()").get()
        print(self.count)
        item =ArticleItem(title=title,avatar=avatar,author=author,pub_time=pub_time,article_id=article_id,
                          word_count=word_count,comment_count=comment_count,
                          read_count=read_count,like_count=like_count,content=content,origin_url=response.url)
        yield item