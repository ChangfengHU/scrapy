#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 23:12
# @Author  : changfeng

from  selenium import webdriver

browser =webdriver.Chrome(executable_path="D:\\code\\scrapy\\chromedriver.exe")
browser.get("http://www.kugou.com/song/tfyesc5.html#hash=C89FDECA500B792965F73B9815204005&album_id=0")
ss=browser.find_element_by_xpath("//audio[@id='myAudio']").get_attribute("src")
print(ss)
browser.quit()
