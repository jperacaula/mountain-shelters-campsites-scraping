# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16, 2022
@author: Sara Jose, Joan Peracaula
"""
import scrapper

def main():
    
    # Get all links for shelter and campsites websites
    headers, all_links = scrapper.get_urls()
    
    # Scrape de attributes
    accommodations_list = scrapper.get_atributes(headers, all_links)
    
    #Save the attributes in a csv
    scrapper.save_dataset(accommodations_list)
    
if __name__ == "__main__":
    main()