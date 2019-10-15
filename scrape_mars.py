# Dependencies
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import splinter
import pymongo
from splinter import Browser
from selenium import webdriver
import time

#def init_browser()
executable_path = {"executable_path": "/Users/mrvis/Downloads/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    # Create empty Dictionary to store the data
    mars_data = {}

    # visit Mars Weather
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve page with the requests module
    #Examine the results, then determine element that contains sought info
    news_title = soup.find("div", class_= "content_title").find("a").text.strip()
    news_paragraph = soup.find("div","article_teaser_body").text
    #print(news_title)
    #print(news_paragraph)

    #adding to dictionary
    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_paragraph

    # visit Mars images
    url_pic = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_pic)
    html_pic = browser.html
    soup = bs(html_pic, "html.parser")
    
    #Examine the results, then determine element that contains sought info
    search_area = soup.find("div", class_= "carousel_items")
    
    # Identify and return URL for the latest image
    url_picb = search_area.a['data-fancybox-href']
    print(url_picb)
    #Combine the two URL's to produce the actual URL for the image
    url_pica = "https://www.jpl.nasa.gov"
    image_url = url_pica + url_picb
    print(image_url)
    #adding to dictionary
    mars_data["featured_image"] = image_url

    # visit Mars twitter
    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)
    html_twitter = browser.html
    soup = bs(html_twitter, "html.parser")

    search_twitter = soup.find_all("div", class_= "js-tweet-text-container")
    #print(search_twitter)

    # Retrieve the weather related tweet
    for tweet in search_twitter: 
        mars_weather = tweet.find('p').text
        if 'Sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
    else: 
        pass
    
    #adding to dictionary
    mars_data["weather"] = mars_weather

    #url_fact = 'https://space-facts.com/mars/'
    # visit Mars twitter
    url_fact = 'https://space-facts.com/mars/'
    browser.visit(url_fact)
    html_facts = browser.html
    soup = bs(html_facts, "html.parser")
    #search_facts = soup.find("table", class_= "tablepress tablepress-id-p-mars")
    tables = pd.read_html(url_fact)
    tables

    df2 = tables[1]
    df2.columns = ['Parameter','Value']
    #html_table1.replace('\n', '')

    html_table2 = df2.to_html()
    html_table2
    facts = html_table2.replace('\n', '')
    
    #adding to dictionary
    mars_data["facts"] = facts

    # visit Mars images
    url_astro = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_astro)
    html_astro = browser.html
    soup = bs(html_astro, "html.parser")


    # Parse HTML with Beautiful Soup and Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')
    # Create empty list for hemisphere urls and Store the main_ul
    astro_image_urls = [] 
    astro_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items
    for i in items: 
        # Store title and link that leads to full image website
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(astro_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        soup = bs(partial_img_html, 'html.parser')
        
        # Retrieve full image source and append the retreived information into a list of dictionaries 
        img_url = astro_main_url + soup.find('img', class_='wide-image')['src']
        astro_image_urls.append({"title" : title, "img_url" : img_url})
        
        # Display hemisphere_image_urls
        astro_image_urls
        # get_ipython().system('ipython nbconvert --to=python mission_to_mars.ipynb')

    #adding to dictionary
    mars_data["hemispheres"] = astro_image_urls


    browser.quit()
    return mars_data 
