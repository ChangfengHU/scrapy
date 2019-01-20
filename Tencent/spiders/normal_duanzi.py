# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import QsbkItem

class DuanziSpider(scrapy.Spider):
    name = 'duanzi'
    allowed_domains = ['qiushibaike.com']
    # 1. 需要拼接的url
    baseURL = "https://www.qiushibaike.com/text/page/"
    # 2. 需要拼接的url地址的偏移量
    offset = 1
    # 3.爬虫启动时，读取的url地址列表
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    start_urls = [baseURL + str(offset)]
    def parse(self, response):
        duanzidivs = response.xpath("//div[@id='content-left']/div")
        print (type(duanzidivs))

        for duanzidiv in duanzidivs:
            author = duanzidiv.xpath(".//h2/text()").get().strip()
            content = duanzidiv.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()
            item = QsbkItem(author=author, content=content)
            yield item
            # #第一种拼接的翻页
            # if self.offset < 13:
            #     self.offset += 1
            #     url = self.baseURL + str(self.offset)
            #     yield scrapy.Request(url, callback = self.parse)
            next_usl=response.xpath("//ul[@class='pagination']/li[last()]/a/@href").extract()[0]
            if next_usl:
                yield scrapy.Request("https://www.qiushibaike.com"+next_usl, callback=self.parse)
            else:
                return
