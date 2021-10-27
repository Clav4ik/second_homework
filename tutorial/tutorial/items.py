# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AutoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    way = scrapy.Field()
    uah_price = scrapy.Field()
    usd_price = scrapy.Field()
    vin = scrapy.Field()
    link = scrapy.Field()
