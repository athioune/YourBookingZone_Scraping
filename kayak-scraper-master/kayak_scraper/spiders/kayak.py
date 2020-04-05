# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy_splash import SplashRequest
import datetime
import json
import re
import string
from datetime import date, timedelta
from ..C_DECLARATION_SEQUENCEMENT_GOOGLE_FLIGHTS import c_declaration_sequencement_google_flights_from_dict

from .. import items

# ********************************************************************************************
# Important: Run -> docker run -p 8050:8050 scrapinghub/splash in background before crawling *
# ********************************************************************************************


# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# ********************************************************************************************

class KayakSpider(scrapy.Spider):
    name = 'kayak'
    allowed_domains = ['www.google.com']
    urlList = []

    '''
    You don't have to override __init__ each time and can simply use self.parameter (See https://bit.ly/2Wxbkd9),
    but I find this way much more readable.
    '''
    def __init__(self, *args,**kwargs):
        super(KayakSpider, self).__init__(*args, **kwargs)
        self.generationUrls()

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def generationUrls(self):

        with open('/home/ec2-user/sequencementScrapingGoogleFlights/declarationSequencementGoogleFlights.json',
                  'r') as file:
            data = file.read().replace('\n', '')

        elements = c_declaration_sequencement_google_flights_from_dict(json.loads(data))

        for element in elements:
            i = 0
            i += 1
            villeDepart = element.ville_depart
            paysArrivee = element.pays_arrivee
            adults = element.nb_adultes
            enfant = element.nb_enfants
            bebeAssis = element.nb_bebe_assis
            bebeGenoux = element.nb_bebe_genoux
            joursGlissants = element.jours_glissants_a_recuperer

            startDate = date.today()
            endDate = startDate + timedelta(days=joursGlissants)

            for single_date in self.daterange(startDate, endDate):
                checkin = single_date.strftime("%Y-%m-%d")

                # Cas Depart (MTL-DESTINATION)
                for aeroportArrivee in paysArrivee:
                    chaineEnfant = self.creationRequeteEnfants(str(bebeGenoux), str(bebeAssis), str(enfant))

                    url = ('https://www.google.com/flights?hl=fr#flt='
                           '{0}.'
                           '{1}.'
                           '{2}'
                           ';c:CAD;e:1;px:'
                           '{3},{4};'
                           'sd:1;t:f;tt:o'
                           )

                    new_url = url.format(villeDepart[0], aeroportArrivee, checkin, str(adults), chaineEnfant)
                    self.urlList.append(new_url)

                # Cas Retour (DESTINATION-MTL)
                for aeroportArrivee in paysArrivee:
                    chaineEnfant = self.creationRequeteEnfants(str(bebeGenoux), str(bebeAssis), str(enfant))

                    url = ('https://www.google.com/flights?hl=fr#flt='
                           '{0}.'
                           '{1}.'
                           '{2}'
                           ';c:CAD;e:1;px:'
                           '{3},{4};'
                           'sd:1;t:f;tt:o'
                           )

                    new_url = url.format(aeroportArrivee, villeDepart[0], checkin, str(adults), chaineEnfant)
                    self.urlList.append(new_url)

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

        for url in self.urlList:
            yield SplashRequest(url=url, callback=self.parse_id,
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

        pattern = "https:\/\/www.google.com\/flights\?hl=fr#flt=([^.]+).([^.]+).([^;]+);c:CAD;e:1;px:([^;]+)"
        match = re.search(pattern, response.url)

        if match:
            depart = match.group(1)
            destination = match.group(2)
            checkin = match.group(3)
            chainePassager = match.group(4)
            listePassager = []
            listePassager = chainePassager.split(',')

            if len(listePassager) == 1:
                adulte = listePassager[0]
                enfants = 0
                bebeAssis = 0
                bebeGenoux = 0
            elif len(listePassager) == 2:
                adulte = listePassager[0]
                enfants = listePassager[1] or 0
                bebeAssis = 0
                bebeGenoux = 0
            elif len(listePassager) == 3:
                adulte = listePassager[0]
                enfants = listePassager[1] or 0
                bebeAssis = listePassager[2] or 0
                bebeGenoux = 0
            elif len(listePassager) == 4:
                adulte = listePassager[0]
                enfants = listePassager[1] or 0
                bebeAssis = listePassager[2] or 0
                bebeGenoux = listePassager[3] or 0

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
                    item['VilleDepart'] = depart
                    item['VilleArrivee'] = destination
                    item['Compagnie'] = result.group(1)
                    item['NbEscale'] = result.group(2)
                    item['DateHeureDepart'] = result.group(3).replace(': ','').replace(' ','') + ' ' + checkin
                    item['DateHeureArrivee'] = result.group(4).replace(': ','')
                    item['DureeEscale'] = result.group(7).replace(' : ','').replace('min','').replace(' ','').replace(' ','')
                    item['NbAdultes'] = adulte
                    item['NbEnfant'] = enfants
                    item['NbBebePlaceAssise'] = bebeAssis
                    item['NbBebePlaceGenoux'] = bebeGenoux
                    item['DureeTotale'] = result.group(6).replace(': ','').replace('min','').replace(' ','').replace(' ','')
                    item['PrixTotal'] = result.group(5).replace('partir de','').replace('$','').replace(' ','').replace('rde','')

                    yield item