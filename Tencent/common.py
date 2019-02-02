# -*- coding: utf-8 -*-
__author__ = 'bobby'
import hashlib
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    #从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums
def extract_num1(text):
    #从字符串中提取出图片
    match_re = re.match("<img .+ src=\'(.+ \.png)\' />", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums
import  requests
def getpicurl(url):
        html = requests.get(url).text
        pic_url = re.findall('img src="(.*?)"', html, re.S)
        for key in pic_url:
            print(key + "\r\n")
if __name__ == "__main__":
    # print (get_md5("http://jobbole.com".encode("utf-8")))
    getpicurl("http://www.mzitu.com/zipai/comment-pag.e-352")