# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrivagoItem(scrapy.Item):
    # define the fields for your item here like:
    SiteWeb = 'Trivago'
    VilleDestination = scrapy.Field()
    DateAllerSejour = scrapy.Field()
    DateRetourSejour = scrapy.Field()
    TimeStampScraping = scrapy.Field()
    PrixParNuit = scrapy.Field()
    PrixTotal = scrapy.Field()
    NbBebe = scrapy.Field()
    NbEnfant = scrapy.Field()
    NbAdulte = scrapy.Field()
    NomHotel = scrapy.Field()
    NbEtoile = scrapy.Field()
    LienVersHotel = scrapy.Field()
    TypeChambre = scrapy.Field()
    ToutInclus = scrapy.Field()
    NotesMoyenne = scrapy.Field()
    pass
