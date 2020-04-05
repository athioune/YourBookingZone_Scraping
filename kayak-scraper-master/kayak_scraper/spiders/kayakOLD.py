# -*- coding: utf-8 -*-
import datetime
import json
import datetime
import time
import collections
import re
import numpy as np
import logging
import sys
import scrapy
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
from kayak_scraper.items import KayakScraperItem
from time import sleep, strftime
from random import randint
from .. import items

# ********************************************************************************************
# Important: Run -> docker run -p 8050:8050 scrapinghub/splash in background before crawling *
# ********************************************************************************************


# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# ********************************************************************************************

class KayakSpider(scrapy.Spider):
    name = 'kayakold'
    allowed_domains = ['www.google.com']

    '''
    You don't have to override __init__ each time and can simply use self.parameter (See https://bit.ly/2Wxbkd9),
    but I find this way much more readable.
    '''
    def __init__(self, depart='', arrivee='',bebeGenoux=0, bebeAssis='', enfant=0, adults=0, checkin='', *args,**kwargs):
        super(KayakSpider, self).__init__(*args, **kwargs)
        self.depart = depart
        self.arrivee = arrivee
        self.bebeAssis = int(bebeAssis)
        self.bebeGenoux = int(bebeGenoux)
        self.enfant = int(enfant)
        self.adults = int(adults)
        self.checkin = checkin

    def creationRequeteEnfants(self, bebeGenoux, bebeAssis, enfant):
        requeteEnfant = ''

        if bebeGenoux == 0 and bebeAssis == 0 and enfant == 0:
            return ''
        else:
            if enfant > 0:
                requeteEnfant += str(bebeGenoux) + ','
            else:
                requeteEnfant += ','
            if bebeGenoux > 0:
                requeteEnfant += str(bebeGenoux) + ','
            else:
                requeteEnfant += ','
            if bebeAssis > 0:
                requeteEnfant += str(bebeAssis) + ','
            else:
                requeteEnfant += ','

            return requeteEnfant.rstrip(',')

    def start_requests(self):
        '''Sends a scrapy request to the designated url price range

        Args:
        Returns:
        '''

        chaineEnfant = self.creationRequeteEnfants(self.bebeGenoux, self.bebeAssis, self.enfant)

        url = ('https://www.google.com/flights?hl=fr#flt='
               '{0}.'
               '{1}.'
               '{2}'
               ';c:CAD;e:1;px:'
               '{3},{4};'
               'sd:1;t:f;tt:o'
               )

        new_url = url.format(self.depart, self.arrivee, self.checkin, self.adults, chaineEnfant)

        print(new_url)
        #new_url = 'https://www.google.com/flights?hl=fr#flt=/m/0h7h6.VRA.2020-01-21;c:CAD;e:1;px:4,2,1,1;sd:1;t:f;tt:o'


        yield SplashRequest(url=new_url, callback=self.parse_id,
                            args={
                                'wait': 9.5,
                                'timeout': 60,  # Timeout to render (default 30 sec)
                                # 'url': Prefilled by plugin
                                # 'baseurl': Base HTML content, relative resources on page referenced acc. to this.,
                                # 'resource_timeout': #Individual resource request timeout value
                                # 'http_method', 'body',
                                # 'js', 'js_source', 'filters', 'allowed_domains', 'allowed_content_types',
                                # 'forbidden_content_types', 'viewport', 'images', 'headers', 'save_args',
                                # 'load_args'
                            },
                            endpoint='render.html',  # optional; could be render.json, render.png
                            # splash_url = SPLASH_URL, #optional; overrides SPLASH_URL
                             # optional
                            )


    def parse_id(self, response):
        '''Parses all the URLs/ids/available fields from the initial json object and stores into dictionary

        Args:
            response: Json object from explore_tabs
        Returns:
        '''
        voyages = response.xpath("//div[@class='gws-flights-results__itinerary-card-summary gws-flights-results__result-item-summary gws-flights__flex-box']")
        for voyage in voyages:
            item = items.KayakScraperItem()
            item['TimeStampScraping'] = str(time.mktime(datetime.datetime.now().timetuple()))

            chaineComplete = voyage.xpath(".//jsl[1]/text()[1]").get()
            chaineComplete = chaineComplete.replace(u'\xa0', u' ')
            #chaineComplete = chaineComplete.replace(u'\xa9', u'e')
            pattern = "Vol ([a-zA-Z ]+) avec ([^.]+).[^:]+([^.]+).[^:]+([^)]+\)).......[^dd]([^.]+).[^:]+([^.]+).Escale de ([^m]+)"

            p = re.compile(pattern)
            result = p.search(chaineComplete)

            item['Compagnie'] = chaineComplete

            if result is not None:
                item['VilleDepart'] = self.depart
                item['VilleArrivee'] = self.arrivee
                item['Compagnie'] = result.group(1)
                item['NbEscale'] = result.group(2)
                item['DateHeureDepart'] = result.group(3).replace(': ','').replace(' ','') + ' ' + self.checkin
                item['DateHeureArrivee'] = result.group(4).replace(': ','')
                item['DureeEscale'] = result.group(7).replace(' : ','').replace('min','').replace(' ','').replace(' ','')
                item['NbAdultes'] = self.adults
                item['NbEnfant'] = self.enfant
                item['NbBebePlaceAssise'] = self.bebeAssis
                item['NbBebePlaceGenoux'] = self.bebeGenoux
                item['DureeTotale'] = result.group(6).replace(': ','').replace('min','').replace(' ','').replace(' ','')
                item['PrixTotal'] = result.group(5).replace('partir de','').replace('$','').replace(' ','').replace('rde','')

                yield item