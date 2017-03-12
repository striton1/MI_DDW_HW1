import scrapy
from cssselect import HTMLTranslator

class Jawamania(scrapy.Spider):
    name = 'jawamania'
    user_agent = 'scrapy'   
    allowed_domains = ['jawamania.info', 'www.jawamania.info']
    download_delay = 1.0
    start_urls = ['http://jawamania.info/poradna/default.aspx']

    def parse(self, response):
       
        for question in response.css('.Question'):

            #food_text = food.css('div.food-text')
	    questionID = question.css('.Information > .ID ::text').extract()
	    category = question.css('.Information > .Category::text').extract()
            title = question.css('.Summary ::text').extract()
	    
	    url = question.css('td > a ::attr(href)').extract_first()

	    author = question.css('td > .Author ::text').extract()
	    date = question.css('td > .Time ::text').extract()
	    
	    questionText = question.css('.Text ::text').extract()
	    hints = question.xpath('//span[@class="RText"]/text()').extract()	

	    
            yield {
		'questionID': questionID,
		'title': title,
		'url': "http://jawamania.info"+url,
		'author': author,
		'category': category,
		'date': date,	
		'questionText': questionText,
 		'hints': hints,

            }

        for next_page in response.css('a ::attr(href)').extract():
            if not next_page.startswith('/users/') and not next_page.startswith('/moto/'):
		yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


