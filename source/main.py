# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16, 2022
@author: Sara Jose, Joan Peracaula
"""
import time
import scraper


def main():
    start_time = time.time()
    print("Scraping...")

    # Get all links for shelter and campsites pages
    all_links = scraper.get_urls()
    
    # Navigate through the links and scrape each accommodation
    accommodations_list = scraper.scrape_accommodations(all_links)
    
    # Save the accomomodations list in a csv file
    scraper.save_dataset(accommodations_list)

    exec_time = time.time() - start_time
    print("Execution time: " + str(round(exec_time/60, 2)) + " minutes")
    

if __name__ == "__main__":
    main()