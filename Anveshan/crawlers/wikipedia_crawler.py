import scrapy
from crawlers.page import Page
from crawlers.helper import filter_text_from_content
from app import socketio

def getWikipediaSpider(url, query, content_id):
	class wikipedia(scrapy.Spider):
		name="wikipedia"	
		allowed_domains = ["wikipedia.org"]
		start_urls=[url]
		
		def parse(self, response):
			print("parsing")
			page = Page()
			page['url'] = response.url
			page['content'] = response.xpath('//div[@id="mw-content-text"]')
			page['content'] = page['content'].xpath('//div[@class="mw-parser-output"]//p//text()').extract()
			#filter content
			text_to_send = filter_text_from_content(page, query)
			#print(text_to_send)
			socketio.emit("content", {'data': text_to_send, "_id": content_id}, broadcast=True)
	return wikipedia