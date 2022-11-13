# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 00:08:11 2022
@author: Sara Jose,  Joan Peracaula
Description: Dynamic web scrapper that longest and shortest route from a shelter

ChromeDriver 107.0.5304.62
Chrome version: Version 107.0.5304.107 (Official Build) (64-bit)
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

def route_scrapper(url):    
   
    #Choose chrome driver from selenium   
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    #(Hard coded, pass url from main function)
    driver_main = driver.get(url)
    
    
    #route2 = driver.find_element(By.LINK_TEXT, "GR-241") 
    #links= driver.find_elements(By.CLASS_NAME, "btn-link")

    GR_links = driver.find_elements(By.PARTIAL_LINK_TEXT, 'GR')
    try:
        GR_name = GR_links[0].text
        GR_links[0].click()
        GR_distance = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[3]/div/div[2]/div[1]/div[1]/div[1]/span').text
        driver_main = driver.get(url)
    except IndexError:
        GR_name = '?'
        GR_distance = '?'

    PR_links = driver.find_elements(By.PARTIAL_LINK_TEXT, 'PR')
    
    try:
        PR_name = PR_links[0].text
        PR_links[0].click()
        PR_distance = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[3]/div/div[2]/div[1]/div[1]/div[1]/span').text
    except IndexError:
        PR_name = '?'
        PR_distance = '?'
    
        
    
    GR = GR_name , GR_distance
    PR = PR_name , PR_distance
    
    return GR, PR

#route2 = driver.find_element(By.LINK_TEXT, "GR-241") 
#route2.click()
