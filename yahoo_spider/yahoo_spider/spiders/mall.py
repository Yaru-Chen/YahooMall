# -*- coding: utf-8 -*-
import scrapy
import re


class MallSpider(scrapy.Spider):
    name = 'mall'
    start_urls = ['https://tw.mall.yahoo.com/']

    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'MONGODB_COLLECTION': 'mall',
        'MONGODB_ITEM_CACHE': 1000
    }

    def parse(self, response):
        for ul in response.dom('.D-ib.Va-t.menu-pop-store .clearfix:even').items():
            for li in ul('li').items():
                pop_store = li.text()
                url = li('a').attr('href')
                yield scrapy.Request(url, callback=self.parse_salerank, meta={'pop_store': pop_store})

    def parse_salerank(self, response):
        href = response.dom("a:contains('購買人次最高')").attr('href')
        if href:
            yield scrapy.Request(response.url + href, callback=self.parse_top,
                                 meta={'pop_store': response.meta['pop_store']})

    def parse_top(self, response):
        for ul in response.dom('#ypsausi .datatitle').nextAll().items():
            for li in ul('li').items():
                yield scrapy.Request(li('p a').attr('href'), callback=self.parse_page,
                                     meta={'pop_store': response.meta['pop_store']})
            if ul[0].tag == 'div':
                break

    def parse_page(self, response):
        pop_store = response.meta['pop_store']
        title = response.dom("h1").text()

        webprice = response.dom(".webprice").text()
        num = response.dom("li:contains('銷售件數')").text()

        if num and webprice:
            price = re.search('(\d+)元', webprice).group(1)
            num = re.search('銷售件數：(\d+)', num).group(1)
            yield {'pop_store': pop_store, 'title': title, 'price': price, 'num': num}


"""
scrapy crawl mall -o mall.csv
scrapy crawl mall -o mall.json
"""
