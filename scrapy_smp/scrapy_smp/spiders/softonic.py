import datetime
import inspect
import scrapy
import re

spider_load_time = datetime.datetime.now(datetime.timezone.utc)
clean_article_regex = re.compile(r'\n|\t| class=\"app-softonic-review__content \"')

def add_meta(item, spider_instance, response):
    item['scrapy_meta'] = {
        'request_time': datetime.datetime.now(datetime.timezone.utc),
        'request_url': response.url,
        'parent_url': response.meta.get('parent_url'),
        'spider_name': spider_instance.name,
        'spider_load_time': spider_load_time,
        'callback_function': inspect.stack()[1][3],
    }
    return item

class SoftonicAppExplore(scrapy.Spider):
    name = 'softonic_app_explore'

    start_urls = [
        # so that mac windows android ios is visible
        'https://en.softonic.com/web-apps',
    ]

    def parse(self, response):
        return self.parse_platform(response)

    def parse_platform(self, response):
        platform_links = response.xpath("//div[@class='list-pulldown-platforms']/ul//a")

        for platform_link in platform_links[0:4]:
            url = platform_link.xpath("@href").extract_first()
            name = platform_link.xpath("@title").extract_first()

            yield add_meta({
                'name': name,
                'type': "platform",
                'url': url
            }, self, response)

            request = scrapy.Request(url, self.parse_category)
            request.meta['parent_url'] = response.url
            request.meta['platform'] = name
            yield request

    def parse_category(self, response):
        category_links = response.xpath("//div[@class='standar_nav']//a")
        platform = response.meta['platform']

        for category_link in category_links:
            url = category_link.xpath("@href").extract_first()
            name = category_link.xpath("@title").extract_first().strip()

            yield add_meta({
                'name': name,
                'type': "category",
                'platform': platform,
                'url': url
            }, self, response)

            request = scrapy.Request(url, self.parse_sub_category)
            request.meta['parent_url'] = response.url
            request.meta['category'] = name
            yield request

    def parse_sub_category(self, response):
        sub_category_links = response.xpath("//div[@id='categories_nav']//a")

        for sub_category_link in sub_category_links:
            url = sub_category_link.xpath("@href").extract_first()
            name = sub_category_link.xpath("@title").extract_first()
            category = response.meta['category']

            yield add_meta({
                'name': name,
                'category': category,
                'type': "sub_category",
                'url': url
            }, self, response)

            request = scrapy.Request(url, self.parse_app_list)
            request.meta['parent_url'] = response.url
            request.meta['category'] = category
            request.meta['sub_category'] = name
            yield request

    def parse_app_list(self, response):
        app_list = response.css("article.app-list-item")
        category = response.meta['category']
        sub_category = response.meta['sub_category']

        if len(response.xpath("//a[contains(@class, 'pagination-links__previous')]")) == 0:
            page_number = 1
        else:
            page_number = int(response.url.split('/')[-1])

        # app_urls = response.xpath("//div[contains(@class, 'content')]/ul/li/a/@href").extract()

        for page_order, app in enumerate(app_list, start = 1):
            yield add_meta({
                'type': "app",
                'category': category,
                'sub_category': sub_category,
                'logo_url': app.css('.media-app__image').xpath('./img/@src').extract_first(),
                'url': app.xpath('./parent::a/@href').extract_first(),
                'name': app.css('.media-app__title::text').extract_first().strip(),
                'version': app.css('.media-app__title').xpath('./span/text()').extract_first(),
                'license': app.css('.media-app__license::text').extract_first().strip(),
                'language': app.css('.media-app__language::text').extract_first(),
                'platform': app.css('.media-app__platform span::text').extract_first(),
                'summary': app.css('.media-app__summary::text').extract_first().strip(),
                'download_count': app.css('.app-list-item__rating div').re_first('([1-9].*) downloads'),
                'score': app.css('.rating-score__number').xpath('./@content').extract_first(),
                'votes': app.css('.app-list-item__rating div').re_first('([0-9]+) votes?'),
                'page_number': page_number,
                'page_order': page_order,
                'pros': app.css('.app-list-item__pro-con--pro::text').extract_first(),
                'cons': app.css('.app-list-item__pro-con--con::text').extract_first()
            }, self, response)

        next_page = response.css('.pagination-links__next').xpath('./@href').extract_first()

        if next_page:
            request = scrapy.Request(next_page, self.parse_app_list)
            request.meta['parent_url'] = response.url
            request.meta['category'] = category
            request.meta['sub_category'] = sub_category
            yield request
