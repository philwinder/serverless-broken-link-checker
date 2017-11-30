import os

import scrapy
from scrapy.item import Item, Field

CHECK_URL = os.environ["URL"]


class BrokenItem(Item):
    url = Field()
    referer = Field()
    status = Field()


class BrokenLinksSpider(scrapy.Spider):
    name = 'broken_link_spider'
    start_urls = [CHECK_URL, ]
    handle_httpstatus_list = [400, 403, 404, 500, 501]

    def parse(self, response):
        if self.error_condition(response):
            yield self.to_item(response)

        # Find links to follow
        for link in response.css('a::attr(href)'):
            url = link.extract()

            # Skip large and/or invalud links.
            invalid_urls = [".mov", ".m4a", "mailto"]
            if any(substring in url for substring in invalid_urls):
                return

            # If a local link, follow links. Else only check response.
            if CHECK_URL in url:
                yield scrapy.Request(response.urljoin(url), callback=self.parse)
            else:
                yield scrapy.Request(response.urljoin(url), callback=self.parse_external)

    def parse_external(self, response):
        if self.error_condition(response):
            yield self.to_item(response)

    def error_condition(self, response):
        error_states = [403, 404]
        if response.status in error_states:
            return True
        return False

    def to_item(self, response):
        item = BrokenItem()
        item['url'] = response.url
        item['referer'] = response.request.headers.get('Referer').decode("utf-8")
        item['status'] = response.status
        return item
