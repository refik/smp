import scrapy
import re

clean_article_regex = re.compile(r'\n|\t| class=\"app-softonic-review__content \"')

class FindAppSpider(scrapy.Spider):
    name = 'app_finder'

    start_urls = ['https://en.softonic.com/windows']

    def parse(self, response):
        category_urls = response.xpath('//div[@class="standar_nav"]//a/@href').extract()

        for url in category_urls:
            yield scrapy.Request(url, self.parse_sub_category)

    def parse_sub_category(self, response):
        sub_category_urls = response.xpath('//div[@id="categories_nav"]//a/@href').extract()

        for url in sub_category_urls:
            yield scrapy.Request(url, self.parse_app_list)

    def parse_app_list(self, response):
        app_urls = response.xpath('//div[contains(@class, "content")]/ul/li/a/@href').extract()

        for url in app_urls:
            yield scrapy.Request(url, self.parse_app)

    def parse_app(self, response):
        review = response.xpath("//article[@class='app-softonic-review__content ']").extract_first()

        if review:
            review = clean_article_regex.sub('', review)

        logo_url = response.\
            xpath('//header/div[contains(@class, "media-app__image")]/img/@src').\
            extract_first()

        app_name = response.xpath("//h1[@class='media-app__title']/text()").extract_first().strip()
        categories = response.xpath("//li[@class='list-tags__item']/a/@title").extract()

        yield {
            'app_name': app_name,
            'logo_url': logo_url,
            'article': review,
            'categories': categories
        }