# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16, 2022
@author: Sara Jose, Joan Peracaula
"""

import os
import sys
import requests
import random
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import attributes_scrapper as scrap

def get_urls():
    headers = {
        "Accept": "text/html",
        "Cache-Control": "no-cache",
        'dnt': '1',
        'upgrade-insecure-requests': '1',   
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Referer": "https://www.walkaholic.me"
    }
    
    # Scrap shelters and campsites landings to obtain a full list of links
    all_links = []
    for landing in ['shelter', 'campsite']:
        page = requests.get('https://www.walkaholic.me/'+landing, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
    
        list_links = soup.find(class_='list-page').find_all('a')
        all_links += ["https://www.walkaholic.me" + a.get('href') for a in list_links]
    
    # Shuffle links to access randomly (more human-like, less prone to be detected by the system)
    random.shuffle(all_links)
        
    return headers, all_links

def get_atributes(headers, all_links):
    accommodations_list = []
    
    for link in all_links[:10]: 
        page = requests.get(link, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Get all attributes
        places_list = scrap.get_country_subregions(soup)
        place_type, name = scrap.get_placetype(soup)
        capacity, fee, altitude = scrap.get_capacity_fee_altitude(soup)
        description= scrap.get_description(soup)
        telephone, website, email, hiking_association, guard_names = scrap.get_contact(soup)
        services_list = scrap.get_services(soup)
        lat_long, access, zones, emplacement = scrap.get_location(soup)
        routes_list = scrap.get_routes(soup)
                       
        # Append new scrapped accomodation to the list
        accommodations_list.append({
                'Place type': place_type, 'Name': name, 'Place list': places_list,
                'Capacity': capacity, 'Fee': fee, 'Altitude': altitude, 'Description': description, 
                'Telephone': telephone, 'Website': website, 'Email': email, 
                'Hiking association': hiking_association, 'Guard name(s)': guard_names, 
                'Services': services_list, 'Coordinates': lat_long, 'Acces': access, 'Zones': zones,
                'Emplacement': emplacement, 'Nearby routes': routes_list
            })        
    
    print("Scrapping complete!")
    return accommodations_list

def save_dataset(accommodations_list):
    
    #Create path for the dataset
    script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    root_path = os.path.dirname(script_path)
    dataset_path = os.path.join(root_path, "dataset/shelters_and_campsites.csv")
    print("Saving dataset to: " + dataset_path) 
    
    # Create pandas dataframe with the whole scrapped data and save it as CSV in the datasets directory 
    df = pd.DataFrame.from_dict(accommodations_list)
    df.to_csv(dataset_path)
