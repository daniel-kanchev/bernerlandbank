import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bernerlandbank.items import Article


class BernerlandbankSpider(scrapy.Spider):
    name = 'bernerlandbank'
    start_urls = ['https://www.bernerlandbank.ch/Blog']

    def parse(self, response):
        links = response.xpath('//a[@class="c7n-button"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1//text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="col-md-12 col-sm-12 col-xs-12 c7n-news-intro"]/strong//text()').get()
        if date:
            date = date.strip()

        content = response.xpath('(//div[@class="col-xs-12"])[1]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
