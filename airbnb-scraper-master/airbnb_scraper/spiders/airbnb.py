# -*- coding: utf-8 -*-
import datetime
import json
import time
import datetime
import collections
import re
import numpy as np
import logging
import sys
import scrapy
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
from airbnb_scraper.items import AirbnbScraperItem


# ********************************************************************************************
# Important: Run -> docker run -p 8050:8050 scrapinghub/splash in background before crawling *
# ********************************************************************************************


# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# ********************************************************************************************

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['www.airbnb.com']

    '''
    You don't have to override __init__ each time and can simply use self.parameter (See https://bit.ly/2Wxbkd9),
    but I find this way much more readable.
    '''
    def __init__(self, lieu='',bebe=0, enfant=0, adults=0, checkin='', checkout='', price_lb='', price_ub='', *args,**kwargs):
        super(AirbnbSpider, self).__init__(*args, **kwargs)
        self.lieu = lieu
        self.bebe = bebe
        self.enfant = enfant
        self.adults = adults
        self.checkin = checkin
        self.checkout = checkout
        self.price_lb = price_lb
        self.price_ub = price_ub

    def start_requests(self):
        '''Sends a scrapy request to the designated url price range

        Args:
        Returns:
        '''
        self.lieu.replace('Republique', 'République')
        self.lieu.replace('Jamaique', 'Jamaïque')
        self.lieu.replace('Caraibes', 'Caraïbes')



        url = ('https://www.airbnb.ca/api/v2/explore_tabs?_format=for_explore_search_web'
               '&_intents=p1'
               '&allow_override%5B%5D='
               '&adults={3}'
               '&auto_ib=false'
               '&checkin={4}'
               '&checkout={5}'
               '&children={2}'
               '&client_session_id=ecff8cd3-6f4e-4bfd-9bc2-99ba0bb47258'
               '&currency=CAD'
               #  '&current_tab_id=home_tab'
               '&experiences_per_grid=20'
               '&fetch_filters=true'
               '&guidebooks_per_grid=20'
               '&has_zero_guest_treatment=true'
               # '&hide_dates_and_guests_filters=false'
               '&infants={1}'
               '&is_guided_search=true'
               '&is_new_cards_experiment=true'
               '&is_standard_search=true'
               '&items_per_grid=18'
               '&key=d306zoyjsyarp7ifhu67rjxn52tv0t20'
               '&locale=en-CA'
               '&luxury_pre_launch=false'
               '&metadata_only=false'
               # '&place_id=ChIJtUx6DwdJzYgRGqQQkVL3jHk'
               '&query={0}'
               '&query_understanding_enabled=true'
               '&refinement_paths%5B%5D=%2Fhomes'
               # '&satori_version=1.1.7'
               '&s_tag=QLb9RB7g'
               # '&screen_height=706'
               # '&screen_size=medium'
               # '&screen_width=902'
               '&search_type=filter_change'
               '&selected_tab_id=home_tab'
               '&show_groupings=true'
               '&supports_for_you_v3=true'
               '&timezone_offset=-240'
               '&version=1.6.5'
               '&price_min={6}'
               '&price_max={7}')
        new_url = url.format(self.lieu, self.bebe, self.enfant, self.adults, self.checkin, self.checkout, self.price_lb, self.price_ub)

        print(new_url)

        yield scrapy.Request(url=new_url, callback=self.parse_id, dont_filter=True)


    def parse_id(self, response):
        '''Parses all the URLs/ids/available fields from the initial json object and stores into dictionary

        Args:
            response: Json object from explore_tabs
        Returns:
        '''

        # Fetch and Write the response data
        data = json.loads(response.body)
        # Return a List of all homes
        homes = data.get('explore_tabs')[0].get('sections')[0].get('listings')

        try:
            if homes is None:
                homes = data.get('explore_tabs')[0].get('sections')[1].get('listings')
            if homes is None:
                homes = data.get('explore_tabs')[0].get('sections')[2].get('listings')
            if homes is None:
                homes = data.get('explore_tabs')[0].get('sections')[3].get('listings')
            if homes is None:
                homes = data.get('explore_tabs')[0].get('sections')[4].get('listings')
            if homes is None:
                homes = data.get('explore_tabs')[0].get('sections')[5].get('listings')
            if homes is None:
                raise CloseSpider("No homes available in the city and price parameters")
        except IndexError:
                raise CloseSpider("No homes available in the city and price parameters")

        base_url = 'https://www.airbnb.com/rooms/'
        # data_dict = collections.defaultdict(dict) # Create Dictionary to put all currently available fields in
        listing = AirbnbScraperItem()

        for home in homes:
            room_id = str(home.get('listing').get('id'))
            url = base_url + str(home.get('listing').get('id'))
            listing = AirbnbScraperItem()

            listing['url'] = url
            listing['price'] = home.get('pricing_quote').get('rate').get('amount')
            listing['bathrooms'] = home.get('listing').get('bathrooms')
            listing['bedrooms'] = home.get('listing').get('bedrooms')
            listing['host_languages'] = self.checkin
            listing['is_business_travel_ready'] = home.get('listing').get('is_business_travel_ready')
            listing['is_fully_refundable'] = home.get('listing').get('is_fully_refundable')
            listing['is_new_listing'] = home.get('listing').get('is_new_listing')
            listing['is_superhost'] = home.get('listing').get('is_superhost')
            listing['lat'] = home.get('listing').get('lat')
            listing['lng'] = home.get('listing').get('lng')
            listing['localized_city'] = home.get('listing').get('localized_city')
            listing['localized_neighborhood'] = home.get('listing').get('localized_neighborhood')
            listing['listing_name'] = home.get('listing').get('name')
            listing['person_capacity'] = home.get('listing').get('person_capacity')
            listing['picture_count'] = home.get('listing').get('picture_count')
            listing['picture_url'] = home.get('listing').get('picture_url')
            listing['reviews_count'] = home.get('listing').get('reviews_count')
            listing['room_type_category'] = home.get('listing').get('room_type_category')
            listing['star_rating'] = home.get('listing').get('star_rating')
            listing['host_id'] = home.get('listing').get('user').get('id')
            listing['avg_rating'] = home.get('listing').get('avg_rating')
            listing['can_instant_book'] = home.get('pricing_quote').get('can_instant_book')
            listing['monthly_price_factor'] = home.get('pricing_quote').get('monthly_price_factor')
            listing['currency'] = home.get('pricing_quote').get('rate').get('currency')
            listing['amt_w_service'] = home.get('pricing_quote').get('rate_with_service_fee').get('amount')
            listing['rate_type'] = home.get('pricing_quote').get('rate_type')
            listing['weekly_price_factor'] = home.get('pricing_quote').get('weekly_price_factor')
            listing['TimeStampScraping'] = str(time.mktime(datetime.datetime.now().timetuple()))
            listing['num_beds'] = home.get('listing').get('beds')
            listing['num_bedrooms'] = home.get('listing').get('bedrooms')

            # Finally return the object
            yield listing

        # After scraping entire listings page, check if more pages
        pagination_metadata = data.get('explore_tabs')[0].get('pagination_metadata')
        if pagination_metadata.get('has_next_page'):
            items_offset = pagination_metadata.get('items_offset')
            section_offset = pagination_metadata.get('section_offset')

            url = ('https://www.airbnb.ca/api/v2/explore_tabs?_format=for_explore_search_web'
                   '&_intents=p1'
                   '&allow_override%5B%5D='
                   '&adults={3}'
                   '&auto_ib=false'
                   '&checkin={4}'
                   '&checkout={5}'
                   '&children={2}'
                   '&client_session_id=ecff8cd3-6f4e-4bfd-9bc2-99ba0bb47258'
                   '&currency=CAD'
                 #  '&current_tab_id=home_tab' 
                   '&experiences_per_grid=20'
                   '&fetch_filters=true'
                   '&guidebooks_per_grid=20'
                   '&has_zero_guest_treatment=true'
                   #'&hide_dates_and_guests_filters=false'
                   '&infants={1}'
                   '&is_guided_search=true'
                   '&is_new_cards_experiment=true'
                   '&is_standard_search=true'
                   '&items_per_grid=18'
                   '&key=d306zoyjsyarp7ifhu67rjxn52tv0t20'
                   '&locale=en-CA'
                   '&luxury_pre_launch=false'
                   '&metadata_only=false'
                   #'&place_id=ChIJtUx6DwdJzYgRGqQQkVL3jHk'
                   '&query={0}'
                   '&query_understanding_enabled=true'
                   '&refinement_paths%5B%5D=%2Fhomes'
                   #'&satori_version=1.1.7'
                   '&s_tag=QLb9RB7g'
                   #'&screen_height=706'
                   #'&screen_size=medium'
                   #'&screen_width=902'
                   '&search_type=filter_change'
                   '&selected_tab_id=home_tab'
                   '&show_groupings=true'
                   '&supports_for_you_v3=true'
                   '&timezone_offset=-240'
                   '&items_offset={6}'
                   '&section_offset={7}'
                   '&version=1.6.5'
                   '&price_min={8}'
                   '&price_max={9}')
            new_url = url.format(self.lieu, self.bebe, self.enfant, self.adults, self.checkin, self.checkout, items_offset, section_offset, self.price_lb, self.price_ub)

            # If there is a next page, update url and scrape from next page
            yield scrapy.Request(url=new_url, callback=self.parse_id, dont_filter=True)
