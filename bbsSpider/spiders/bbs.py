
# -*- coding:utf8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from bbsSpider.items import BbsspiderItem
from scrapy.exceptions import CloseSpider
from scrapy.http import FormRequest


class BbsSpider(Spider):
    """docstring for bbsSpider"""
    name = "bbsSpider"
    start_urls = [r'http://m.byr.cn/board/ParttimeJob?p=1',
                 r'http://m.byr.cn/board/ParttimeJob?p=2',
                 r'http://m.byr.cn/board/ParttimeJob?p=3',
                 r'http://m.byr.cn/board/ParttimeJob?p=4',
                 r'http://m.byr.cn/board/ParttimeJob?p=5',]
    header ={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }
    def start_requests(self):
        print 'start_requests'
        return [Request("http://m.byr.cn/", callback=self.post_login)]

    def post_login(self, response):
        _data = {'id':'y120141447',
                'passwd':'asdwe123',
                }
        print 'post_login'
        return [FormRequest.from_response(response, headers = self.header, formdata=_data, callback = self.after_login, dont_filter=True)]

    def after_login(self, response):
        print 'after_login'
        for url in self.start_urls:
            yield self.make_requests_from_url(url)


    def parse(self, response):
        print 'success'
        print response.url
        selector = Selector(response)
        tbody = selector.xpath('//li')
        for each in tbody:
            href = each.xpath('div/a/@href').extract()[0]
            title = each.xpath('div/a/text()').extract()[0]
            item = BbsspiderItem()
            item['url'] = href
            item['title'] = title
            url = "http://m.byr.cn" + href
            yield Request(url=url, callback=self.parseContent, meta={'item': item})

    def parseContent(self, response):
        print "Get"
        selector = Selector(response)
        item = response.meta['item']
        html = selector.xpath('//div[@class="sp"]').extract()[0]
        time = selector.xpath(
            '//*[@id="m_main"]/ul/li[2]/div[1]/div[1]/a[3]/text()').extract()[0]
        item['time'] = time
        item['html'] = html
        print time
        yield item
