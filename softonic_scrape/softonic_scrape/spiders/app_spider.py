import scrapy
import re

class AppSpider(scrapy.Spider):
    name = 'app'

    start_urls = [
        'https://amazon-compras.softonic.com/android',
        'https://moboplay.en.softonic.com/'
    ]

    clean_regex = re.compile(r'\n|\t| class=\"app-softonic-review__content \"')

    def parse(self, response):
        review_node = response.xpath("//article[@class='app-softonic-review__content ']")
        review = self.clean_regex.sub('', review_node.extract_first())
        app_name = response.xpath("//h1[@class='media-app__title']/text()").extract_first()
        yield {
            'app_name': app_name,
            'article': review
        }