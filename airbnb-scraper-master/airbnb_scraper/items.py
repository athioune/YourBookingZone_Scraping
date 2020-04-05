# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def remove_unicode(value):
    return value.replace(u"\u201c", '').replace(u"\u201d", '').replace(u"\2764", '').replace(u"\ufe0f")

class AirbnbScraperItem(scrapy.Item):

    url = scrapy.Field()
    price = scrapy.Field()
    bathrooms = scrapy.Field()
    bedrooms = scrapy.Field()
    host_languages = scrapy.Field()
    is_business_travel_ready = scrapy.Field()
    is_fully_refundable = scrapy.Field()
    is_new_listing = scrapy.Field()
    is_superhost = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    localized_city = scrapy.Field()
    localized_neighborhood = scrapy.Field()
    listing_name = scrapy.Field(input_processor=MapCompose(remove_unicode))
    person_capacity = scrapy.Field()
    picture_count = scrapy.Field()
    picture_url = scrapy.Field()
    reviews_count = scrapy.Field()
    room_type_category = scrapy.Field()
    star_rating = scrapy.Field()
    host_id = scrapy.Field()
    avg_rating = scrapy.Field()
    can_instant_book = scrapy.Field()
    monthly_price_factor = scrapy.Field()
    currency = scrapy.Field()
    amt_w_service = scrapy.Field()
    rate_type = scrapy.Field()
    weekly_price_factor = scrapy.Field()
    TimeStampScraping = scrapy.Field()
    num_beds = scrapy.Field()
    num_bedrooms = scrapy.Field()


