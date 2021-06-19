import chompjs
import scrapy


class ListingsSpider(scrapy.Spider):
    name = "listings"
    
    def start_requests(self):
        url = 'https://streeteasy.com/for-rent/astoria?view=map'
        yield scrapy.Request(url=url, callback=self.get_listing_ids)
        
    def get_listing_ids(self, response):
        script = response.css("script:contains('dataLayer =')::text")
        obj = chompjs.parse_js_object(script.get())
        listing_ids = obj[0]["searchResultsListings"].split("|")
        yield {"ids": listing_ids}
        