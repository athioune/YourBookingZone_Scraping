# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def remove_unicode(value):
    return value.replace(u"\u201c", '').replace(u"\u201d", '').replace(u"\2764", '').replace(u"\ufe0f")

class KayakScraperItem(scrapy.Item):
    SiteWeb = 'Google Flights'
    VilleDepart = scrapy.Field()
    VilleArrivee = scrapy.Field()
    DateHeureDepart = scrapy.Field()
    DateHeureArrivee = scrapy.Field()
    Compagnie = scrapy.Field()
    NbAdultes = scrapy.Field()
    DureeEscale = scrapy.Field()
    NbEnfant = scrapy.Field()
    NbBebePlaceAssise = scrapy.Field()
    NbBebePlaceGenoux = scrapy.Field()
    NbEscale = scrapy.Field()
    DureeTotale = scrapy.Field()
    PrixTotal = scrapy.Field()
    TimeStampScraping = scrapy.Field()


