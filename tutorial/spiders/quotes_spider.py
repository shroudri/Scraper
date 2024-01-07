import scrapy
import datetime

class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')

        # Extract quotes
        for quote in quotes:
            yield {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": {
                    "text": quote.xpath(".//span[@class='text']/text()").get(),
                    "author": quote.xpath(".//small[@class='author']/text()").get(),
                    "tags": quote.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall(),
                }
            }

        # Navigate to next page
        next_page_btn = response.xpath('//li[@class="next"]/a').attrib["href"]
        if next_page_btn:
            yield response.follow(next_page_btn, callback=self.parse)

        pass
