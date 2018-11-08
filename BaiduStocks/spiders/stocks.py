import scrapy
import re

class stocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            try:
                stock = re.findall('[s][zh]\d{6}', href)[0]
                url = 'http://gupiao.baidu.com/stock/' + stock + '.html'
                yield scrapy.Request(url, callback=self.parse_stock)
            except:
                continue

    def parse_stock(self, response):
        infoDict = {}
        stockInfo = response.css('.stock-bets')  #只搜索'.stock-bets'标签下的'dt'和'dd'标签
        stockname = stockInfo.css('.bets-name').extract()
        keyList = stockInfo.css('dt').extract()
        valueList = stockInfo.css('dd').extract()
        for i in range(len(keyList)):
            key = re.findall('<dt.*?>(.*?)</dt>', keyList)[0]
            try:
                value = re.findall('<dd.*?>(.*?)</dd>', valueList)[0]
            except:
                value = '--'
            infoDict[key] = value
        infoDict.update({'股票名称': re.findall('<a.*?">(.*?)(<span.*?)', stockname)})
        yield infoDict
