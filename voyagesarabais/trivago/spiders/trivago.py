# -*- coding: utf-8 -*-
import time
import datetime
import json
import collections
import re
import numpy as np
import logging
import sys
import scrapy
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
from .. import items
import base64

# ********************************************************************************************
# Important: Run -> docker run -p 8050:8050 scrapinghub/splash in background before crawling *
# ********************************************************************************************

# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# *********************************************************************************************

class QuotesSpider(scrapy.Spider):
    name = "trivago"
    allowed_domains = ['www.trivago.ca']

    '''
        You don't have to override __init__ each time and can simply use self.parameter (See https://bit.ly/2Wxbkd9),
        but I find this way much more readable.
        '''

    def __init__(self, arrivee='', date='', duree='', age1='', age2='', age3='', age4='', *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        #self.depart = 'YUL'
        #self.arrivee = 'f'
        #self.date = '2019-12-15'
        #self.duree = '7day%2C8day'

        self.arrivee = arrivee
        self.date = date
        self.duree = duree
        self.age1 = age1
        self.age2 = age2
        self.age3 = age3
        self.age4 = age4

    def start_requests(self):
        url = ('https://voyagesarabais.com/recherche-sud?' \
              'gateway={0}' \
              '&destDep={1}' \
              '&dateDep={2}' \
              '&duration={3}' \
              '&bedrooms%5B0%5D%5B0%5D={4}' \
              '&bedrooms%5B0%5D%5B1%5D={5}' \
              '&bedrooms%5B0%5D%5B2%5D={6}' \
              '&bedrooms%5B0%5D%5B3%5D={7}' \
              '&bedrooms%5B0%5D%5B4%5D=' \
              '&bedrooms%5B0%5D%5B5%5D=' \
              '&noHotel=' \
              '&star=0' \
              '&starmax=5' \
              '&flexlow=3' \
              '&flexhigh=3')

        url = ('https://www.trivago.ca/?'
               'aDateRange%5Barr%5D=2019-12-21'
               '&aDateRange%5Bdep%5D=2019-12-26'
               '&aPriceRange%5Bfrom%5D=0'
               '&aPriceRange%5Bto%5D=0'
               '&iRoomType=9'
               '&aRooms%5B0%5D%5Badults%5D=2'
               '&aRooms%5B0%5D%5Bchildren%5D%5B0%5D=3'
               '&aRooms%5B0%5D%5Bchildren%5D%5B1%5D=1'
               '&aRooms%5B0%5D%5Bchildren%5D%5B2%5D=14'
               '&cpt2=105%2F200'
               '&iViewType=0'
               '&bIsSeoPage=0'
               '&sortingId=1'
               '&slideoutsPageItemId='
               '&iGeoDistanceLimit=20000'
               '&address='
               '&addressGeoCode='
               '&offset=0&ra=')
        new_url = url

        yield SplashRequest(new_url, self.parse,
            endpoint='render.html',
            args={'wait': 4.0},
        )

    def calculNbPersonne(self, age1, age2, age3, age4):
        NbBebe = 0
        NbEnfant = 0
        NbAdulte = 0
        my_list = [age1, age2, age3, age4]
        for age in my_list:
            if age is None or age == '' or age == '0':
                continue
            elif int(age) < 2:
                NbBebe += 1
            elif int(age) < 16:
                NbEnfant += 1
            else:
                NbAdulte += 1

        return NbBebe, NbEnfant, NbAdulte

    def parse(self, response):
        # response.body is a result of render.html call; it
        # contains HTML processed by a browser.
        # …
        NbBebe = 0
        NbEnfant = 0
        NbAdulte = 0
        NbBebe, NbEnfant, NbAdulte = self.calculNbPersonne(self.age1, self.age2, self.age3, self.age4)

        voyages = response.xpath("//li[@class='hotel-item item-order__list-item js_co_item']")
        for voyage in voyages:
            item['VilleDestination'] = voyage.xpath(".//p[@class='details-paragraph details-paragraph--location location-details']/text()").get()
            item['DateAllerSejour'] = self.dateDepart
            item['DateRetourSejour'] = self.dateArrivee
            item['TimeStampScraping'] = str(time.mktime(datetime.datetime.now().timetuple()))
            item['PrixTotal'] = voyage.xpath(".//strong[@class='item__best-price price_min item__best-price--perstay']/text()").get()
            item['PrixParNuit'] = voyage.xpath(".//strong[@class='item__per-night fs-normal']/text()").get()
            item['NbBebe'] = NbBebe
            item['NbEnfant'] = NbEnfant
            item['NbAdulte'] = NbAdulte
            item['NomHotel'] = voyage.xpath(".//span[@class='item-link name__copytext']/text()").get()
            item['NbEtoile'] = ''
            item['LienVersHotel'] =
            item['TypeChambre'] = voyage.xpath(".//span[@class='item__accommodation-type']/text()").get()
            item['ToutInclus'] = ''
            item['NotesMoyenne'] = voyage.xpath(".//span[@itemprop='ratingValue']/text()").get()



            destination = voyage.xpath(".//h3[@class='searchresultdestname']/text()").get()
            dureeJours = voyage.xpath(".//div[@class='minicard_text clearfix'][1]/p[1]/text()[1]").get().replace('\n', ' ').replace('\r', '')
            nomHotel = voyage.xpath(".//h3[@class='searchresulthotelname'][1]/a[1]/text()[1]").get()
            nbEtoile = float(len(voyage.xpath(".//div[@class='minicard_stars stars_float'][1]//img[@src='/img/icon/icon_color_goldstar.svg']"))) \
                       + \
                       (1.0*float((len(voyage.xpath(".//div[@class='minicard_stars stars_float'][1]//img[@src='/img/icon/icon_color_goldstar_half.svg']"))//2)))

            chambres = voyage.xpath(".//div[@class='click_box other_room no_var_rate']")

            item = items.TrivagoItem()
            item['DateAllerSejour'] =
            item['DateRetourSejour'] =
            item['TypeChambre'] = chambre.xpath("//*/@data-room-type").get().strip()
            item['TimeStampScraping'] = str(time.mktime(datetime.datetime.now().timetuple()))
            item['VilleDestination'] = destination

            except:
                item['DateAllerSejour'] = ''
                item['DureeSejour'] = ''
                item['PrixTotal'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' total_price ')]/p[@class='mini_price']/text()").get().strip()
                item['PrixTotal'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' total_price ')]/p[@class='mini_price']/text()").get()
                item['Ristourne'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' mini_block_ristourne ')]/p[@class='mini_price']/text()").get()
            item['NbBebe'] = NbBebe
            item['NbEnfant'] = NbEnfant
            item['NbAdulte'] = NbAdulte
            item['NomHotel'] = nomHotel
            item['NbEtoile'] = nbEtoile
            item['LienVersHotel'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' border_left ')]/a[1]/@href").get()

            if 'Tout Inclus' in item['TypeChambre']:
                item['ToutInclus'] = 'Oui'
            else:
                item['ToutInclus'] = 'Non'



            #Faire un callback


            if item['PrixTotal'] is not None:
                yield item

