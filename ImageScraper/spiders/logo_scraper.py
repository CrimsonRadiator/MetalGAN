import scrapy
import json
from ImageScraper.items import ImagescraperItem

class LogoScraper(scrapy.Spider):
    name='logos'
    def start_requests(self):
        urls = [f'https://www.metal-archives.com/browse/ajax-genre/g/black/json/1?sEcho=1&iDisplayStart={n}' for n in range(1000, 37571, 500)]
        #urls = ['https://www.metal-archives.com/browse/ajax-genre/g/black/json/1?sEcho=1&iDisplayStart=0']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseBandList)

    def parseBandList(self, response):
        jsonResponse = json.loads(response.text)

        for band in jsonResponse['aaData']:
            bandUrl = band[0]
            bandUrl = bandUrl.split('\'')[1]

            yield scrapy.Request(url=bandUrl, callback=self.parseBand)
    
    def parseBand(self, response):
        imageUrl = response.css('#logo').css('img::attr(src)').get()
        bandName = response.css('.band_name').css('a::text').get()
        if imageUrl and bandName:
            item = ImagescraperItem()
            item['image_urls'] = [imageUrl]
            item['band_name'] = bandName
            return item