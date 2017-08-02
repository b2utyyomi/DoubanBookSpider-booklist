# -*- coding: utf-8 -*-
import scrapy
import re
from doubanbook.items import DoubanbookItem

class DbbookSpider(scrapy.Spider):
    name = "dbbook"
    #allowed_domains = ["https://www.douban.com/doulist/1264675/"]
    start_urls = (
        'https://www.douban.com/doulist/1264675/',
    )
    URL = 'https://www.douban.com/doulist/1264675/?start=PAGE&sort=seq&sub_type='
    def parse(self, response):
        #print response.body
        item = DoubanbookItem()
        selector = scrapy.Selector(response)
        books = selector.xpath('//div[@class="bd doulist-subject"]')
        for each in books:
            title = each.xpath('div[@class="title"]/a/text()').extract()
            if title:
                title = title[0]
            else:
                title = ""
            rate = each.xpath('div[@class="rating"]/span[@class="rating_nums"]/text()').extract()
            if rate:
                rate = rate[0]
            else:
                rate = ''
            person_num = each.xpath('div[@class="rating"]/span/text()').extract()
            if len(person_num)>=2:
                person_num = person_num[1]
            else:
                person_num = ''
            author = re.search('<div class="abstract">(.*?)<br',each.extract(),re.S).group(1)
            title = title.replace(' ','').replace('\n','')
            author = author.replace(' ','').replace('\n','')
            item['title'] = title
            item['rate'] = rate
            item['author'] = author
            item['person_num'] = person_num
            # print 'title:' + title
            # print 'rate:' + rate
            # print author
            # print ''
            yield item
            nextPage = selector.xpath('//span[@class="next"]/a/@href').extract()
            if nextPage:
                next = nextPage[0]
                print(next)
                yield scrapy.http.Request(next,callback=self.parse)

