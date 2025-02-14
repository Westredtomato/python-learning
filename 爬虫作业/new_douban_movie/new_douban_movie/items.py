# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewDoubanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    no = scrapy.Field()  # 电影编号
    title = scrapy.Field()  # 电影标题
    link = scrapy.Field()  # 电影链接
    director = scrapy.Field()  # 导演
    score = scrapy.Field()  # 评分
    comment = scrapy.Field()  # 评论数
    summary = scrapy.Field()  # 简介
    pass