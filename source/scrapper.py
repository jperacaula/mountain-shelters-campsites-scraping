import requests
import random
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

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
    
shelters_list = []
for link in all_links[:10]: 

    page = requests.get(link, headers=headers)  # Change Referer header to the previous link (?)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Extract country and subregions
    breadcrump = soup.find_all(class_='breadcrumb-item')
    places_list = [x.find('a').contents[0].strip() for x in breadcrump]  # Country, region, subregion (the last could be null)

    # Extract place type and name
    head = soup.find(class_='name').contents[0].strip()
    place_type, name = head.split(" - ", maxsplit=1)

    # Extract capacity, fee and altitude if available
    div_basic_details = soup.find(class_='basic-details')
    capacity, fee, altitude = '?', '?', '?'
    if div_basic_details.find(class_='capacity'):  # Apparently, capacity shouldn't be null
        capacity = div_basic_details.find(class_='capacity').find_next('span').contents[0]

    if div_basic_details.find(class_='fee'):  # Apparently, fee shouldn't be null
        fee = div_basic_details.find(class_='fee').find_next('span').contents[0]
    
    if div_basic_details.find(class_='altitude'):  # Altitude could be null
        altitude = div_basic_details.find(class_='altitude').find_next('span').contents[0]

    # Extract description, if available
    description = '?'
    if soup.find(class_='description'):
        description = soup.find(class_='description').contents[0]

    # Extract Contact information if available
    telephone, website, email, hiking_association, guard_names = '?', '?', '?', '?', '?'
    div_contact = soup.find(class_='contact')
    if div_contact:
        div_contact.find(class_='row').decompose()  # Exclude first row with title (required for better extracting next contents that don't have unique CSS classes)

        if div_contact.find(class_='link telephone'):
            telephone = div_contact.find(class_='link telephone')['href']
            div_contact.find(class_='link telephone').find_parent().decompose()  # Exclude this element (required for better extracting next contents that don't have unique CSS classes)

        if div_contact.find(class_='link website'):
            website = div_contact.find(class_='link website')['href']   
            div_contact.find(class_='link website').find_parent().decompose()  # Exclude this element (required for better extracting next contents that don't have unique CSS classes)

        if div_contact.find(class_='link email'):
            email = div_contact.find(class_='link email')['href']
            div_contact.find(class_='link email').find_parent().decompose()  # Exclude this element (required for better extracting next contents that don't have unique CSS classes)

        # Extract Hiking association and Guard name(s), if available
        hiking_association, guard_names = '?', '?'
        extra_rows = div_contact.find_all(class_='row')
        for row in extra_rows:
            label = row.find('b').contents[0]
            if label == 'Hiking association:':
                hiking_association = label.next.strip()
            elif label == 'Guard name(s):':
                guard_names = label.next.strip()

    # Extract list of services, if available
    services_list = []
    if soup.find(class_='service'):
        services = soup.find_all(class_='service')
        for service in services:
            services_list.append(service['title'])    
             
    # Extract Location/'How to get there' information
    lat_long = '?'
    access, zones, emplacement = [], [], []
    div_access = soup.find(class_='how-to-get-there')
    if div_access:
        div_access.find(class_='row').decompose()  # Decompose title row
        
        # Get latitude and longitude
        if div_access.find(class_='row'):
            div_access.find(class_='col-12').decompose()
            lat_long = div_access.find(class_='row coordinates').find_next('span').contents[0]
            div_access.find(class_='row coordinates').decompose()
        
        # Get acces, zones and emplacement
        if div_access.find(class_='row'):
            for row in div_access.find_all(class_='row'):
                text = row.text.replace("\n", "")
                
                if text.startswith('Zone'):
                    zones.append(text)
        
                elif text.startswith('Emplacement'):
                    emplacement.append(text)
                    
                elif text.startswith('Access'):
                    access.append(text) 

    # Extract Nearby hiking routes names
    routes_list = []
    routes = soup.find("div", class_='nearby-routes')
    if routes:
        for a in routes.find_all('a', href=True):
            routes_list.append(a.text.strip())
                   
    # Append new scrapped shelter to the list
    shelters_list.append({'Place type': place_type, 'Name': name, 'Place list': places_list,
                    'Capacity': capacity, 'Fee': fee, 'Altitude': altitude, 'Description': description, 
                    'Telephone': telephone, 'Website': website, 'Email': email, 
                    'Hiking association': hiking_association, 'Guard name(s)': guard_names, 
                    'Services': services_list, 'Coordinates': lat_long, 'Acces': access, 'Zones': zones,
                    'Emplacement': emplacement, 'Nearby routes': routes_list})


# Create pandas dataframe with the whole scrapped data and save it as CSV in the datasets directory 
df = pd.DataFrame.from_dict(shelters_list)
df.to_csv("../dataset/shelters.csv")
