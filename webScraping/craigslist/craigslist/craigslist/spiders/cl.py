import scrapy
from craigslist.items import CraigslistItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup as bs

class CraigslistSpider(CrawlSpider):

	name = 'clCrawl'

	start_urls = ['https://sfbay.craigslist.org/search/rva?min_price=100']

	#Defining rule to crawl next pages

	rules = (Rule(LinkExtractor(restrict_xpaths = ['//a[@title="next page"]']),follow=True,callback='parse_data'),)

	def parse_data(self,response):
		prices = response.xpath('//span[@class="result-meta"]/span[@class="result-price"]/text()').extract()

		#price = response.xpath('//*[@class = "price"]/text()').extract()[0]
		links = response.xpath('//p/a/@href').extract()
		listings = response.xpath('//p/a[@class="result-title hdrlnk"]/text()').extract()

		for price,link,listing in zip(prices,links,listings):
			item = CraigslistItem()
			item['price'] = price
			item['link'] = "https://sfbay.craigslist.org" + str(link)
			item['listing'] = listing
			yield item
