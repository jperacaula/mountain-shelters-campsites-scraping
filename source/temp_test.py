# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 22:52:41 2022

@author: sara-
"""
import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
from tabulate import tabulate

        # TODO: Extract Services information
        # Services list                    
            
        # TODO: Extract Location/How to get there information
        # Latitude, longitude
        # Acces, zone
headers = {
    "Accept": "text/html",
    "Cache-Control": "no-cache",
    'dnt': '1',
    'upgrade-insecure-requests': '1',   
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Referer": "https://www.walkaholic.me"
}

# Shelters links list
page = requests.get('https://www.walkaholic.me/shelter/spain/catalonia/girona/3-refugi-coma-de-vaca', headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

  
div_access = soup.find(class_='how-to-get-there')
if div_access:
    div_access.find(class_='row').decompose()
    

    #Get latitude and longitude
    if div_access.find(class_='row'):
        div_access.find(class_='col-12').decompose()
        lat_long = div_access.find(class_='row coordinates').find_next('span').contents[0]
        div_access.find(class_='row coordinates').decompose()
        print(lat_long)
        print()
    
    if div_access.find(class_='row'):
        div_access.find(class_='col-12').decompose()
        rows = div_access.find_all(class_='row')
        access = []
        zones = []
        emplacement = []
        
        for row in rows:
            text = row.text.replace("\n", "")
            
            if text.startswith('Zone'):
                zones.append(text)

            elif text.startswith('Emplacement'):
                emplacement.append(text)
                
            else:
                access.append(text) 
            
        #find_next('span').contents[0]
        #div_access.find(class_='row coordinates').find_parent().decompose()
        print(access)
        print(zones)
        print(emplacement)
            