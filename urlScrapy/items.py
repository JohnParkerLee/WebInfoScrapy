# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # 1 icp_list
    web_name = scrapy.Field()  # 网站名称
    web_home = scrapy.Field()  # 首页网址
    com_name = scrapy.Field()  # 主办单位
    icp_type = scrapy.Field()  # 单位性质
    icp_no = scrapy.Field()  # 网站备案/许可证号

    # 2 server_list
    server_ip = scrapy.Field()  # 服务器ip
    server_location = scrapy.Field()  # ip所在地
    http_type = scrapy.Field()  # 协议类型
    server_type = scrapy.Field()  # 服务器类型
    content_type = scrapy.Field()  # 页面类型

    # 3 whois_list
    domain = scrapy.Field()  # 域名
    reg_server = scrapy.Field()  # 注册商
    server = scrapy.Field()  # whois服务器
    nserver = scrapy.Field()  # dnf服务器
    create_day = scrapy.Field()  # 创建时间

    # 4 rank_list
    world_rank = scrapy.Field()  # 全球排名
    world_uv_rank = scrapy.Field()  # 访客排名
    country_code = scrapy.Field()  # 国家/地区
    country_rank = scrapy.Field()  # 国家/地区排名

    # 5 chart
    rank_trend_chart = scrapy.Field()  # 排名走势图链接
    search_proportion_chart = scrapy.Field()  # 搜索流量占比图链接

