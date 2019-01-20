# -*- coding: utf-8 -*-
import scrapy


class RenrenLoginSpider(scrapy.Spider):
    name = 'renren_login'
    allowed_domains = ['renren.com']
    start_urls = ['http://renren.com/']
    def start_requests(self):
        url = "http://www.renren.com/PLogin.do"
        data={"email":"970138074@qq.com","password":"pythonspider"}
        request=scrapy.FormRequest(url,formdata=data,callback=self.parse_page)
        yield request
    def parse_page(self, response):
        url='http://www.renren.com/880151247/profile';
        request=scrapy.Request(url, callback=self.parse_profile)
        yield request
    def parse_profile(self, response):
        with open("data/renren_profile.html", "w", encoding='utf-8') as fd:
            fd.write(response.text)

