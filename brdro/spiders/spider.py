import scrapy

from scrapy.loader import ItemLoader
from ..items import BrdroItem
from itemloaders.processors import TakeFirst


class BrdroSpider(scrapy.Spider):
	name = 'brdro'
	start_urls = ['https://www.brd.ro/despre-brd/noutati-si-presa/ultimele-noutati']

	def parse(self, response):
		post_links = response.xpath('//div[@class="content news"]/div/div/div/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="pager-next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="articol"]//text()[normalize-space() and not(ancestor::h1 | ancestor::p[@class="date"] | ancestor::div[@class="fixed-menu"] | ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="date"]/text()').get()

		item = ItemLoader(item=BrdroItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
