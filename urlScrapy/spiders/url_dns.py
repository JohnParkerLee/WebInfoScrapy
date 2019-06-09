# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from bs4 import BeautifulSoup
import re
import json
import requests
from ..items import UrlscrapyItem
import urllib

gHeads = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
}

class UrlDnsSpider(scrapy.Spider):
    name = "url_dns"
    start_urls = ['http://www.alexa.cn/siterank/']

    def parse(self, response):
        # <a /a>标签中的所有链接

        select = Selector(text=response.text)
        url_list = select.xpath(
            "//ul[@class='siterank-sitelist']//li//div[2]//div[1]/a[1]")

        for ul in url_list:
            now_url = ul.xpath("string(.)").extract()[0]
            url = 'http://www.alexa.cn/' + now_url
            # print(url)
            yield scrapy.Request(url, meta={'item': now_url}, callback=self.parse_url)

        # 下一页
        print("------------------------================Next Page=================-----------------\n")
        cur_page = response.xpath(
            "//strong[@class='current']/text()").extract_first()
        cur_page = int(cur_page)
        # 一共只有100页
        if cur_page < 3:
            next_url = 'http://www.alexa.cn/siterank/' + str(cur_page + 1)
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

            
    def parse_url(self, response):
        print("---------------------------------=================================-----------------\n")
        p = r"token.+?,"
        pattern1 = re.compile(p)
        # matcher = re.match(p,response.text)
        temp = pattern1.findall(response.text)
        result = []
        for i in temp:
            result.append(i.split('\'')[1])
        print(result)

        payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}
        search_url = response.meta['item']
        # 1. ICP备案信息
        html1 = "http://www.alexa.cn/api/icp/info?token=" + \
                result[0] + "&url=" + search_url + "&host=&vcode="
        # 2. 服务器与首页基本信息
        html2 = "http://www.alexa.cn/api/server/get?token=" + \
                result[1] + "&url=" + search_url + "&force_update=0"
        # 3. Whois注册信息
        html3 = "http://www.alexa.cn/api/who_is/get?token=" + \
                result[2] + "&url=" + search_url + "&force_update=0"
        # 4.排名
        html4 = "http://www.alexa.cn/api/alexa/free?token=" + \
                result[3] + "&url=" + search_url
        # 5. 图片
        pic1 = 'http://traffic.alexa.com/graph?o=lt&y=q&b=ffffff&n=666666&f=999999&p=4e8cff&r=1y&t=2&z=0&c=1&h=150&w=340&u=qq.com' + search_url
        pic2 = 'http://traffic.alexa.com/graph?y=t&b=ffffff&n=666&f=999999&r=7d&t=2&z=30&c=1&h=280&w=920&u=' + search_url

        ret1 = requests.get(html1, data=json.dumps(payload), headers=headers)
        ret2 = requests.get(html2, data=json.dumps(payload), headers=headers)
        ret3 = requests.get(html3, data=json.dumps(payload), headers=headers)
        ret4 = requests.get(html4, data=json.dumps(payload), headers=headers)
        icp = json.loads(ret1.text)
        server = json.loads(ret2.text)
        whois = json.loads(ret3.text)
        rank = json.loads(ret4.text)
        icp_list = [icp['data']['web_name'], icp['data']['web_home'],
                    icp['data']['com_name'], icp['data']['icp_type'], icp['data']['icp_no']]
        server_list = [server['data']['server_ip'], server['data']['server_location'],
                       server['data']['http_type'], server['data']['server_type'], server['data']['content_type']]
        whois_list = [whois['data']['domain'], whois['data']['reg_server'],
                      whois['data']['server'], whois['data']['nserver'][0], whois['data']['create_day']]
        rank_list = [rank['data']['world_rank'],
                     rank['data']['world_uv_rank'], rank['data']['country_code'], rank['data']['country_rank']]
        pic_list = [pic1, pic2]

        items = UrlscrapyItem()

        items['web_name'] = icp_list[0]
        items['web_home'] = icp_list[1]
        items['com_name'] = icp_list[2]
        items['icp_type'] = icp_list[3]
        items['icp_no'] = icp_list[4]

        items['server_ip'] = server_list[0]
        items['server_location'] = server_list[1]
        items['http_type'] = server_list[2]
        items['server_type'] = server_list[3]
        items['content_type'] = server_list[4]

        items['domain'] = whois_list[0]
        items['reg_server'] = whois_list[1]
        items['server'] = whois_list[2]
        items['nserver'] = whois_list[3]
        items['create_day'] = whois_list[4]

        items['world_rank'] = rank_list[0]
        items['world_uv_rank'] = rank_list[1]
        items['country_code'] = rank_list[2]
        items['country_rank'] = rank_list[3]

        items['rank_trend_chart'] = pic_list[0]
        items['search_proportion_chart'] = pic_list[1]

        print(icp_list)
        print(server_list)
        print(whois_list)
        print(rank_list)
        print(pic_list)
        yield items
