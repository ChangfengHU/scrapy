# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Tencent.items import KugouMusicItem


class KugouSpider(CrawlSpider):
    name = 'kugou'
    allowed_domains = ['kugou.com']
    start_urls = ['http://kugou.com/']
    count=0
    # https://www.kugou.com/yy/album/single/14275743.html
    # https://www.kugou.com/yy/special/single/580534.html
    # http://www.kugou.com/song/t2ow2a5.htm
    # https://www.kugou.com/yy/special/single/580534.html
    rules = (
    # https://www.kugou.com/yy/rank/home/1-6666.htm%E3%80%81
    Rule(LinkExtractor(allow=r'.+/yy/album/single/.+\.html'),follow=True),
    # Rule(LinkExtractor(allow=r'.+/yy/rank/home/.+\.html.+'),follow=True),
    Rule(LinkExtractor(allow=r'.+song/'),follow=False,callback="parse_detail"),
    )

    def parse_detail(self, response):
        self.count=self.count+1;
        print(response.url)
        url=response.xpath("//audio[@id='myAudio']").get()
        url1 = response.xpath("//div[@class='author']/a[@class='avatar']/img/@src").get()
        print(url)
        item = KugouMusicItem(category=response.url,url=url)
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        yield item;
