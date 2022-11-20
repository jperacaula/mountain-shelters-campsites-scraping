# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16, 2022
@author: Sara Jose, Joan Peracaula
"""
import os
import sys
import time
import scraper
import pandas as pd


def save_dataset(accommodations_list):
    # Create path for the dataset
    script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    project_root_path = os.path.dirname(script_path)
    dataset_path = os.path.join(project_root_path, "dataset/shelters_and_campsites.csv")
    print("Saving dataset to: " + dataset_path) 
    
    # Create pandas dataframe with the whole scraped data and save it as CSV in the datasets directory 
    df = pd.DataFrame.from_dict(accommodations_list)
    df.to_csv(dataset_path)


def main():
    start_time = time.time()
    print("Scraping...")

    # Get all links for shelter and campsites pages
    all_links = scraper.get_urls()
    
    # Navigate through the links and scrape each accommodation
    accommodations_list = scraper.scrape_accommodations(all_links)
    
    # Save the accomomodations list in a csv file
    save_dataset(accommodations_list)

    exec_time = time.time() - start_time
    print("Execution time: " + str(round(exec_time/60, 2)) + " minutes") 
    

if __name__ == "__main__":
    main()