# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from Tencent.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
from Tencent.models.model import Article
from w3lib.html import remove_tags
from w3lib.html import remove_tags
import scrapy
import datetime
import re
class TencentItem(scrapy.Item):
    #职位名
    positionName = scrapy.Field()

    #职位详情连接
    positionLink = scrapy.Field()

    #职位类别
    positionType = scrapy.Field()

    #招聘人数
    peopleNumber = scrapy.Field()

    #工作地点
    workLocation = scrapy.Field()

    #发布时间
    publishTime = scrapy.Field()


class QsbkItem(scrapy.Item):
    author = scrapy.Field()
    content = scrapy.Field()

class DouyuItem(scrapy.Item):
    # 主播昵称
    nickname = scrapy.Field()
    # 图片链接
    imagelink = scrapy.Field()

class BmwItem(scrapy.Item):
    category = scrapy.Field()
    image_urls = scrapy.Field()
#   item =ArticleItem(title=title,avatar=avatar,author=author,pub_time=pub_time,article_id=article_id,content=content,origin_url=response.url)


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    avatar = scrapy.Field()
    author = scrapy.Field()
    pub_time = scrapy.Field()
    article_id = scrapy.Field()
    word_count = scrapy.Field()
    comment_count = scrapy.Field()
    read_count = scrapy.Field()
    like_count = scrapy.Field()
    content = scrapy.Field()
    origin_url = scrapy.Field()
class KugouMusicItem(scrapy.Item):
    category = scrapy.Field()
    url = scrapy.Field()




class ArticleItemLoader(ItemLoader):
    #自定义itemloader 去list中的第一个
    # 如果不需要处理就自己写output_processor
    # 如果需要所有的数据 则用join 转成字符串
    # input_processor 是数据预处理
    default_output_processor = TakeFirst()

def add_jobbole(value):
    return value+"-bobby"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

def return_value(value):
    return value


def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value
#连接es
from elasticsearch_dsl.connections import connections
# es=connections.create_connection(Article._doc_type.using)
es=connections.create_connection(hosts=["127.0.0.1"], timeout=20)

def gen_suggest(index,info_tople):
    #根据字符串生成搜索建议 数组
    used_words=()
    suggests =[]
    for text,weight in info_tople :
        if text:
            #调用es的analyze接口分析字符串
            # words=es.indices.analyze(index=index,analyzer="ik_max_word",params={'filter':["lowercase"]},body=text)
            words = es.indices.analyze(index=index, body={'text': text, 'analyzer': "ik_max_word"},params={'filter': ["lowercase"]})
            token_list=set(r["token"] for  r in words["tokens"] if len(r["token"])>1)
            new_words=token_list
        else:
            new_words=set()
        if  new_words:
            suggests.append({"input":list(new_words),"weight":weight})
    return suggests
class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(lambda x:x+"_scrapy"),
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field()



    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(title, url,url_object_id, create_date, fav_nums, front_image_url, front_image_path,
            praise_nums, comment_nums, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE fav_nums=fav_nums+1
        """

        fron_image_url = ""
        # content = remove_tags(self["content"])
        # if len(self.fields["front_image_path"])==0:
        #     self["front_image_path"]="123456"
        #获取的就是个list所以单独处理
        if self["front_image_url"]:
            fron_image_url = self["front_image_url"][0]
        params = (self["title"], self["url"], self["url_object_id"], self["create_date"], self["fav_nums"],
                  fron_image_url, self["front_image_path"], self["praise_nums"], self["comment_nums"],
                  self["tags"])
        return insert_sql, params

    def save_to_es(self):
        article = Article()
        article.title = self["title"]
        article.create_date = self["create_date"]
        #内容去标签remove_tags
        article.content = remove_tags(self["content"]).strip().replace("\r\n", "").replace("\t", "")
        article.front_image_url = self["front_image_url"]
        if "front_image_path" in self:
            article.front_image_path = self["front_image_path"]
        article.praise_nums = self["praise_nums"]
        article.comment_nums = self["comment_nums"]
        article.fav_nums = self["fav_nums"]
        article.url = self["url"]
        article.tags = self["tags"]
        article.id = self["url_object_id"]
        article.suggest=gen_suggest("jobbole",((article.title,10),(article.tags,7)))
        article.save()