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
    name = "voyagesarabais"
    allowed_domains = ['www.voyagesarabais.com']

    '''
        You don't have to override __init__ each time and can simply use self.parameter (See https://bit.ly/2Wxbkd9),
        but I find this way much more readable.
        '''

    def __init__(self, depart='', arrivee='', date='', duree='', age1='', age2='', age3='', age4='', *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        #self.depart = 'YUL'
        #self.arrivee = 'f'
        #self.date = '2019-12-15'
        #self.duree = '7day%2C8day'

        self.depart = depart
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
        new_url = url.format(self.depart, self.arrivee , self.date, self.duree, self.age1, self.age2, self.age3, self.age4)

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

        voyages = response.xpath("//div[@class='minicard_element card clearfix js-hotel relative']")
        for voyage in voyages:
            destination = voyage.xpath(".//h3[@class='searchresultdestname']/text()").get()
            dureeJours = voyage.xpath(".//div[@class='minicard_text clearfix'][1]/p[1]/text()[1]").get().replace('\n', ' ').replace('\r', '')
            nomHotel = voyage.xpath(".//h3[@class='searchresulthotelname'][1]/a[1]/text()[1]").get()
            nbEtoile = float(len(voyage.xpath(".//div[@class='minicard_stars stars_float'][1]//img[@src='/img/icon/icon_color_goldstar.svg']"))) \
                       + \
                       (1.0*float((len(voyage.xpath(".//div[@class='minicard_stars stars_float'][1]//img[@src='/img/icon/icon_color_goldstar_half.svg']"))//2)))

            image1 = voyage.xpath(".//img[@class='img_responsive'][1]/@src").get()

            chambres = voyage.xpath(".//div[@id='js-first-room']")
            for chambre in chambres:
                item = items.VoyagesarabaisItem()

                item['Image1'] = image1

                if self.depart == 'YUL':
                    item['VilleDepart'] = 'Montreal'
                else:
                    item['VilleDepart'] = 'Toronto'

                item['TimeStampScraping'] = str(time.mktime(datetime.datetime.now().timetuple()))
                item['VilleDestination'] = destination
                try:
                    item['DateAllerSejour'] = " ".join(re.search(r'([\d]+[\s\w\W]+)[ ]+-[ ]+([\d]+[\s\w\W]+)', dureeJours).group(1).split())
                    item['DureeSejour'] = " ".join(re.search(r'([\d]+[\s\w\W]+)[ ]+-[ ]+([\d]+[\s\w\W]+)', dureeJours).group(2).split())
                except:
                    item['DateAllerSejour'] = ''
                    item['DureeSejour'] = ''
                try:
                    infoVolAller = chambre.xpath(
                        ".//div[contains(concat(' ',normalize-space(@class),' '),' itinary_fly hidden-xs ')]/p[1]").get().replace(
                        '\n', ' ').replace('\r', '')
                    infoVolRetour = chambre.xpath(
                        ".//div[contains(concat(' ',normalize-space(@class),' '),' itinary_fly hidden-xs ')]/p[2]").get().replace(
                        '\n', ' ').replace('\r', '')
                    item['AllerDateHeureDepart'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolAller).group(2).split())
                    item['AllerDateHeureArrivee'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolAller).group(4).split())
                    item['AllerAeroportDepart'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolAller).group(1).split())
                    item['AllerAeroportArrivee'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolAller).group(3).split())
                    item['RetourDateHeureDepart'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolRetour).group(2).split())
                    item['RetourDateHeureArrivee'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolRetour).group(4).split())
                    item['RetourAeroportDepart'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolRetour).group(1).split())
                    item['RetourAeroportArrivee'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolRetour).group(3).split())
                except:
                    item['AllerDateHeureDepart'] = ''
                    item['AllerDateHeureArrivee'] = ''
                    item['AllerAeroportDepart'] = ''
                    item['AllerAeroportArrivee'] = ''
                    item['RetourDateHeureDepart'] = ''
                    item['RetourDateHeureArrivee'] = ''
                    item['RetourAeroportDepart'] = ''
                    item['RetourAeroportArrivee'] = ''
                try:
                    item['PrixParPersonne'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' per_person_price ')]/p[@class='mini_price']/text()").get().strip()
                    item['PrixTotal'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' total_price ')]/p[@class='mini_price']/text()").get().strip()
                    item['Ristourne'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' mini_block_ristourne ')]/p[@class='mini_price']/text()").get().strip()
                except:
                    item['PrixParPersonne'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' per_person_price ')]/text()").get()
                    item['PrixTotal'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' total_price ')]/p[@class='mini_price']/text()").get()
                    item['Ristourne'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' mini_block_ristourne ')]/p[@class='mini_price']/text()").get()
                item['NbBebe'] = NbBebe
                item['NbEnfant'] = NbEnfant
                item['NbAdulte'] = NbAdulte
                item['NomHotel'] = nomHotel
                item['NbEtoile'] = nbEtoile
                item['LienVersHotel'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' border_left ')]/a[1]/@href").get()
                item['TypeChambre'] = re.sub(' +', ' ',chambre.xpath(".//h3[contains(concat(' ',normalize-space(@class),' '),' ex ')]/text()").get().replace(
                        '\n', ' ').replace('\r', '')).strip()
                if 'Tout Inclus' in item['TypeChambre']:
                    item['ToutInclus'] = 'Oui'
                else:
                    item['ToutInclus'] = 'Non'

                if item['PrixTotal'] is not None:
                    yield item



            chambres = voyage.xpath(".//div[@class='click_box other_room no_var_rate']")
            for chambre in chambres:
                item = items.VoyagesarabaisItem()

                item['Image1'] = image1

                item['TypeChambre'] = chambre.xpath("//*/@data-room-type").get().strip()
                item['TimeStampScraping'] = str(time.mktime(datetime.datetime.now().timetuple()))

                if self.depart == 'YUL':
                    item['VilleDepart'] = 'Montreal'
                else:
                    item['VilleDepart'] = 'Toronto'

                item['VilleDestination'] = destination
                try:
                    item['DateAllerSejour'] = " ".join(re.search(r'([\d]+[\s\w\W]+)[ ]+-[ ]+([\d]+[\s\w\W]+)', dureeJours).group(1).split())
                    item['DureeSejour'] = " ".join(re.search(r'([\d]+[\s\w\W]+)[ ]+-[ ]+([\d]+[\s\w\W]+)', dureeJours).group(2).split())
                except:
                    item['DateAllerSejour'] = ''
                    item['DureeSejour'] = ''
                try:
                    infoVolAller = chambre.xpath(
                        ".//div[contains(concat(' ',normalize-space(@class),' '),' itinary_fly hidden-xs ')]/p[1]").get().replace(
                        '\n', ' ').replace('\r', '')
                    infoVolRetour = chambre.xpath(
                        ".//div[contains(concat(' ',normalize-space(@class),' '),' itinary_fly hidden-xs ')]/p[2]").get().replace(
                        '\n', ' ').replace('\r', '')
                    item['AllerDateHeureDepart'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolAller).group(2).split())
                    item['AllerDateHeureArrivee'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolAller).group(4).split())
                    item['AllerAeroportDepart'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolAller).group(1).split())
                    item['AllerAeroportArrivee'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolAller).group(3).split())
                    item['RetourDateHeureDepart'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolRetour).group(2).split())
                    item['RetourDateHeureArrivee'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolRetour).group(4).split())
                    item['RetourAeroportDepart'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolRetour).group(1).split())
                    item['RetourAeroportArrivee'] = " ".join(re.search(r'<img [^>]+>[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)vers[ ]+([a-z A-Z()]+)([a-z A-Z()\d\W]+)<\/p>', infoVolRetour).group(3).split())
                except:
                    item['AllerDateHeureDepart'] = ''
                    item['AllerDateHeureArrivee'] = ''
                    item['AllerAeroportDepart'] = ''
                    item['AllerAeroportArrivee'] = ''
                    item['RetourDateHeureDepart'] = ''
                    item['RetourDateHeureArrivee'] = ''
                    item['RetourAeroportDepart'] = ''
                    item['RetourAeroportArrivee'] = ''
                try:
                    item['PrixParPersonne'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' per_person_price ')]/p[@class='mini_price']/text()").get().strip()
                    item['PrixTotal'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' total_price ')]/p[@class='mini_price']/text()").get().strip()
                    item['Ristourne'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' mini_block_ristourne ')]/p[@class='mini_price']/text()").get().strip()
                except:
                    item['PrixParPersonne'] = chambre.xpath(".//div[contains(concat(' ',normalize-space(@class),' '),' per_person_price ')]/text()").get()
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


                if item['PrixTotal'] is not None:
                    yield item

