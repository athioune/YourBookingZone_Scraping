# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VoyagesarabaisItem(scrapy.Item):
    # define the fields for your item here like:
    SiteWeb = 'Voyages a Rabais'
    VilleDepart = scrapy.Field()
    VilleDestination = scrapy.Field()
    DateAllerSejour = scrapy.Field()
    DureeSejour = scrapy.Field()
    Image1 = scrapy.Field()
    AllerDateHeureDepart = scrapy.Field()
    AllerDateHeureArrivee = scrapy.Field()
    RetourDateHeureDepart = scrapy.Field()
    RetourDateHeureArrivee = scrapy.Field()
    AllerAeroportDepart = scrapy.Field()
    RetourAeroportDepart = scrapy.Field()
    AllerAeroportArrivee = scrapy.Field()
    RetourAeroportArrivee = scrapy.Field()
    TimeStampScraping = scrapy.Field()
    PrixParPersonne = scrapy.Field()
    PrixTotal = scrapy.Field()
    Ristourne = scrapy.Field()
    NbBebe = scrapy.Field()
    NbEnfant = scrapy.Field()
    NbAdulte = scrapy.Field()
    NomHotel = scrapy.Field()
    NbEtoile = scrapy.Field()
    LienVersHotel = scrapy.Field()
    TypeChambre = scrapy.Field()
    ToutInclus = scrapy.Field()
    pass
