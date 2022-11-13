# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 00:08:11 2022
@author: Sara Jose,  Joan Peracaula
Description: Web scrapper that saves data from shelters to a csv
"""

import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
import dynamic_scrapper

def main():
    headers = {
        "Accept": "text/html",
        "Cache-Control": "no-cache",
        'dnt': '1',
        'upgrade-insecure-requests': '1',   
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Referer": "https://www.walkaholic.me"
    }
    
    # Shelters links list
    page = requests.get('https://www.walkaholic.me/shelter', headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    list_page = soup.find(class_='list-page')
    
    all_list_items = list_page.find_all('a')
    all_links = ["https://www.walkaholic.me" + item.get('href') for item in all_list_items]
    
    # Shuffle links to access randomly (more human-like, less prone to be detected by the system)
    random.shuffle(all_links)
    
    #Create an empty dataframe to save all the scraped information
    df = pd.DataFrame(columns=['Link', 'Place list', 'Place type','Name', 'Capacity','Fee', 'Altitude', 'Telephone', 'PR route', 'GR route'])
    
    for link in all_links[:10]: 
        page = requests.get(link, headers=headers)  # Change Referer header to the previous link (?)
        soup = BeautifulSoup(page.text, 'html.parser')
    
        # Extract country and subregions
        breadcrump = soup.find_all(class_='breadcrumb-item')
        places_list = [x.find('a').contents[0].strip() for x in breadcrump]  # Country, region, subregion (the last could be null)
        
        #Remove extra words
        places_list =  {place.replace('Shelter in ', '') for place in places_list}
    
        # Extract place type and name
        head = soup.find(class_='name').contents[0].strip()
        place_type, name = head.split(" - ", maxsplit=1)
    
        # Extract capacity, fee, altitude an telephone if available
        div_basic_details = soup.find(class_='basic-details')
        div_contact = soup.find(class_='mt-2')
        
        capacity, fee, altitude, telephone = '?', '?', '?', '?'
        if div_basic_details.find(class_='capacity'):  # Apparently, capacity shouldn't be null
            capacity = div_basic_details.find(class_='capacity').find_next('span').contents[0]
    
        if div_basic_details.find(class_='fee'):  # Apparently, fee shouldn't be null
            fee = div_basic_details.find(class_='fee').find_next('span').contents[0]
        
        if div_basic_details.find(class_='altitude'):  # Altitude could be null
            altitude = div_basic_details.find(class_='altitude').find_next('span').contents[0]
              
        if  div_contact.find(class_='link telephone'):
            telephone = div_contact.find('a')['href']   
    
        print(link)
        print(places_list)
        print(place_type + ", " + name)
        print(capacity + ", " + fee + ", " + altitude)
        print(telephone)
        print()
    
        routes = '?'
        routes = dynamic_scrapper.route_scrapper(link)    
        df = df.append({'Link': link, 'Place list': places_list, 'Place type': place_type, 'Name': name, 
                        'Capacity': capacity, 'Fee': fee, 'Altitude': altitude, 'Telephone': telephone , 
                        'Routes': routes}, ignore_index=True)
                    
    df.to_csv("refugisdemuntanya.csv")

if __name__ == "__main__":
    main()