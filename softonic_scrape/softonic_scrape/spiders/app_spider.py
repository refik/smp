import scrapy
import re

clean_article_regex = re.compile(r'\n|\t| class=\"app-softonic-review__content \"')

class AppSpider(scrapy.Spider):
    name = 'app'

    start_urls = [
        'https://skim.en.softonic.com/mac',
        'https://moboplay.en.softonic.com/',
        'https://the-unarchiver.en.softonic.com/mac'
    ]

    clean_regex = re.compile(r'\n|\t| class=\"app-softonic-review__content \"')

    def parse(self, response):
        review_node = response.xpath("//article[@class='app-softonic-review__content ']")
        review = clean_article_regex.sub('', review_node.extract_first())

        logo_url = response.\
            xpath('//header/div[contains(@class, "media-app__image")]/img/@src').\
            extract_first()

        app_name = response.xpath("//h1[@class='media-app__title']/text()").extract_first()

        yield {
            'app_name': app_name,
            'logo_url': logo_url,
            'article': review
        }