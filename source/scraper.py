# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16, 2022
@author: Sara Jose, Joan Peracaula
"""

import requests
import random
from bs4 import BeautifulSoup
import accommodation_scraper as accom_scrapper


# Set custom headers with same values as navigation from a web browser
# Important headers to prevent being blocked are: 
#  - User-Agent: don't use the default from requests library, and set a browser-like one (Firfox browser on a Mac OS)
#  - Referer: this header tells the server from where we come from. Setting a logical referer can help to not seem suspicious. In our case, we have set the Walkaholic home URL.
#  - The other headers have browser-like values, trying to imitate a request from a common web browser.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ca,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://www.walkaholic.me/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "TE": "trailers"
}


def get_urls():
    # Scrap shelters and campsites landings to obtain a full list of links
    all_links = []
    for landing in ['shelter', 'campsite']:
        page = requests.get('https://www.walkaholic.me/'+landing, headers=HEADERS)
        soup = BeautifulSoup(page.text, 'html.parser')
    
        list_links = soup.find(class_='list-page').find_all('a')
        all_links += ["https://www.walkaholic.me" + a.get('href') for a in list_links]
    
    # Shuffle links to access randomly (more human-like, less prone to be detected by the system)
    random.shuffle(all_links)
        
    return all_links


def scrape_accommodations(all_links):
    accommodations_list = []
    
    for link in all_links: 
        page = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Get all attributes
        places_list = accom_scrapper.get_country_subregions(soup)
        place_type, name = accom_scrapper.get_placetype(soup)
        capacity, fee, altitude = accom_scrapper.get_capacity_fee_altitude(soup)
        description= accom_scrapper.get_description(soup)
        telephone, website, email, hiking_association, guard_names = accom_scrapper.get_contact(soup)
        services_list = accom_scrapper.get_services(soup)
        lat_long, access, zones, emplacement = accom_scrapper.get_location(soup)
        routes_list = accom_scrapper.get_routes(soup)
                       
        # Append new scraped accomodation to the list
        accommodations_list.append({
                'Place type': place_type, 'Name': name, 'Place list': places_list,
                'Capacity': capacity, 'Fee': fee, 'Altitude': altitude, 'Description': description, 
                'Telephone': telephone, 'Website': website, 'Email': email, 
                'Hiking association': hiking_association, 'Guard name(s)': guard_names, 
                'Services': services_list, 'Coordinates': lat_long, 'Acces': access, 'Zones': zones,
                'Emplacement': emplacement, 'Nearby routes': routes_list
            })        
    
    print("Scraping complete!")
    return accommodations_list
