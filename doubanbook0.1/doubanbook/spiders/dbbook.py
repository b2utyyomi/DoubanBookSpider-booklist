# -*- coding: utf-8 -*-
import scrapy
import re
from doubanbook.items import DoubanbookItem
#import main   #main函数开头就说了两行调用程序的代码，你也可以在cmd中使用scrapy crawl field -o info.csv -t csv来调用。主要是方便
import pymysql     #python3连接数据库的模块pymysql

def store(title, author, rate, person_num):    #调用这个自定义函数来实现对数据库的操作
    cur.execute("ALTER DATABASE scraping CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci")
    cur.execute("ALTER TABLE pages CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cur.execute("ALTER TABLE pages CHANGE title title VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cur.execute("ALTER TABLE pages CHANGE author author VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cur.execute("ALTER TABLE pages CHANGE rate rate VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cur.execute("ALTER TABLE pages CHANGE person_num person_num VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cur.execute("INSERT INTO pages (title, author, rate, person_num) VALUES (\"%s\", \"%s\", \"%s\", \"%s\")", (title, author, rate, person_num))
    connect.commit()   #我们需要提交数据库，否则数据还是不能上传的
    
connect = pymysql.connect(
    user = "root",
    password = "512008226226",  #连接数据库，不会的可以看我之前写的连接数据库的文章
    port = 3306,
    host = "127.0.0.1",
    db = "mysql",
    charset = "utf8"
    )
cur = connect.cursor()  #获取游标
#cur.execute("create database dbbook")  #创建数据库，！！！！这一条代码仅限第一次使用，有了数据库后就不用再使用了
cur.execute("use dbbook")   #使用数据库
cur.execute("drop table if exists pages")  #判断是否存在这个数据库表
sql = '''create table pages(title varchar(1000),author varchar(1000),rate varchar(1000),person_num varchar(1000))'''
cur.execute(sql)  #执行sql命令  创建dbbook表来保存信息
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
            store(title, author, rate, person_num)
            #item['title'] = title
            #item['rate'] = rate
            #item['author'] = author
            #item['person_num'] = person_num
            # print 'title:' + title
            # print 'rate:' + rate
            # print author
            # print ''
            #yield item
            nextPage = selector.xpath('//span[@class="next"]/a/@href').extract()
            if nextPage:
                next = nextPage[0]
                print(next)
                yield scrapy.http.Request(next,callback=self.parse)
            else:
                cur.close()   #关闭游标
                connect.close()  #关闭数据库
                print("OK!!!!!!!!!")   
            



