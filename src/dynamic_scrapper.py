# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 00:08:11 2022
@author: Sara Jose,  Joan Peracaula
Description: Dynamic web scrapper that saves images of the maps for each shelter and gets its closests routes

ChromeDriver 107.0.5304.62
Chrome version: Version 107.0.5304.107 (Official Build) (64-bit)
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def route_scrapper(url):
   
    #Choose chrome driver from selenium   
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver_main = driver.get(url)    
    
    # Get map images of each one of the shelters (uncomment to activate)
    #get_images(driver, url)
    
    #Get nearby routes
    try:
        routes_section = driver.find_element(By.CLASS_NAME, "nearby-routes")
        routes = routes_section.find_elements(By.TAG_NAME, "a")
        routes_names = []
        
        for route in routes:
            routes_names.append(route.text)            
        
    except IndexError:
        routes_names = '?'
    
    driver.quit()
    return routes_names


def get_images(driver, url):
    # Map zoom in    
    zoom = driver.find_element(By.CLASS_NAME, "maplibregl-ctrl-zoom-in")
    for var in list(range(2)):
        zoom.click()
        time.sleep(0.1)
    
    # Map screenshot
    time.sleep(1.2)
    mapa = driver.find_element(By.CLASS_NAME, "maplibregl-canvas")
    
    png_path = "images/" + url.split("/")[-1] + ".png"
    mapa.screenshot(png_path)    