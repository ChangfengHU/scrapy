#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/20 3:59
# @Author  : changfeng


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/20 3:52
# @Author  : changfeng
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text,connections
from elasticsearch_dsl import Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
# 自己定时一个分词器 继承CustomAnalyzer
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}
#     lowercase 忽略大小写 使搜索更加准确1
ik_analyzer = CustomAnalyzer('ik_max_word',filter=['lowercase'])
class Article(DocType):
    # 文章类型
    # 特殊类型Completion 跟text差不多只是搜索建议的专属类型

    suggest = Completion(analyzer=ik_analyzer)

    title = Text(analyzer="ik_max_word")
    create_date = Date()

    url = Keyword()
    id = Keyword()

    front_image_url = Keyword()
    front_image_path = Keyword()

    praise_nums = Integer()
    comment_nums = Integer()
    fav_nums = Integer()

    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = "jobbole"
        doc_type = 'article'
    class Index:
        name = 'jobbole'
        doc_type = 'article'

# connections.create_connection(hosts=["172.16.191.79"], timeout=20)

connections.create_connection(
        hosts=["47.97.247.78"],
        http_auth=('elastic', '36yes58no!@#'),
        port=9200,
        timeout=5000)
# doc = Article(title="你好",url_object_id='121312',praise_nums=1221)
# doc.save()


if __name__ == '__main__':
    Article.init()