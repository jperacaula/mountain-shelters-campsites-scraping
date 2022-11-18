# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16, 2022
@author: Sara Jose, Joan Peracaula
"""


def get_country_subregions(soup):
    # Extract country and subregions
    breadcrump = soup.find_all(class_='breadcrumb-item')
    places_list = [x.find('a').contents[0].strip() for x in breadcrump]  # Country, region, subregion (the last could be null)
    
    return places_list


def get_placetype(soup):  
    # Extract place type and name
    head = soup.find(class_='name').contents[0].strip()
    place_type, name = head.split(" - ", maxsplit=1)
    
    return place_type, name


def get_capacity_fee_altitude(soup):
    # Extract capacity, fee and altitude if available
    div_basic_details = soup.find(class_='basic-details')
    capacity, fee, altitude = '?', '?', '?'
    if div_basic_details.find(class_='capacity'):  # Apparently, capacity shouldn't be null
        capacity = div_basic_details.find(class_='capacity').find_next('span').contents[0]
    
    if div_basic_details.find(class_='fee'):  # Apparently, fee shouldn't be null
        fee = div_basic_details.find(class_='fee').find_next('span').contents[0]
    
    if div_basic_details.find(class_='altitude'):  # Altitude could be null
        altitude = div_basic_details.find(class_='altitude').find_next('span').contents[0]

    return capacity, fee, altitude


def get_description(soup):
    # Extract description, if available
    description = '?'
    if soup.find(class_='description'):
        description = soup.find(class_='description').contents[0]
        
    return description


def get_contact(soup):
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

    return telephone, website, email, hiking_association, guard_names


def get_services(soup):
    # Extract list of services, if available
    services_list = []
    if soup.find(class_='service'):
        services = soup.find_all(class_='service')
        for service in services:
            services_list.append(service['title'])    
     
    return services_list


def get_location(soup):
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
            
    return lat_long, access, zones, emplacement 


def get_routes(soup):   
    # Extract Nearby hiking routes names
    routes_list = []
    routes = soup.find("div", class_='nearby-routes')
    if routes:
        for a in routes.find_all('a', href=True):
            routes_list.append(a.text.strip())
        
    return routes_list
