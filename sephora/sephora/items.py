# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SephoraItem(scrapy.Item):
     brand_name = scrapy.Field()
     brand_link = scrapy.Field()
     item_name = scrapy.Field()
     item_link = scrapy.Field()
     item_ID = scrapy.Field()
     item_category = scrapy.Field()
     item_brand = scrapy.Field()
     item_price = scrapy.Field()
     item_size = scrapy.Field()
     item_loveCount = scrapy.Field()
     item_reviewCount = scrapy.Field()
     item_rating = scrapy.Field()
    
