# Import Dependencies
import requests
import pandas as pd
import time 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
from splinter.exceptions import ElementDoesNotExist



# Create an empty dict. to store the scrapped data 
scraped_data = {}

def init_browser():

    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Declare and assign variable to the page you are scraping
    nasa_url = "https://mars.nasa.gov/news/""

    # Use splinter to open up the nasa url assigned to nasa_url variable
    browser.visit(nasa_url)



    # Create a html object
    nasa_html = browser.htmll

    # Parse (extract necessary components) of html with bs
    beautifulSoup = bs(nasa_html, "html.parser")


   # Retrieve the latest element that contains news title and news_paragraph
    title = beautifulSoup.find_all('div', class_='content_title')[0].text
    paragraph = beautifulSoup.find_all('div', class_='article_teaser_body')[0].text
   
    # Save scrapped data in empty dict 
    scraped_data['newsTitle'] = title
    scraped_data['newsParagraph'] = paragraph
    
    # Return scraped_data
    return scraped_data

    # Use quit funct. to stop browser
    browser.quit()

   # Assign and declare a variable for the featured image
    featuredImage ="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Produce featured image
    browser.visit(featuredImage)

    # Use time.sleep function to slowdown execution by two seconds
    time.sleep(2)

    # Create a html object in preparation of getting the full address of the featured image
    html_image = browser.html

    # Parse html with bs
    beautifulSoupImage = bs(html_image, 'html.parser')

    # Isolate image url from style tag 
    beautifulSoupImage_url  = beautifulSoupImage.find('article') 'style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Concatenate website url with the beautifulSoupImage_url
    beautifulSoupImage_url = 'https://www.jpl.nasa.gov' + beautifulSoupImage_url
    
    # Save full link to featured image

    scraped_data['beautifulSoupImage_url'] = beautifulSoupImage_url


   


    # Assign and declare a variable to represent Mars Weather Twitter
    marsWeather = 'https://twitter.com/marswxreport?lang=en'

    # Use .visit from Splinter to isolate the content of marsWeather
    browser.visit(marsWeather)

    # Use time.sleep function to slowdown execution by two seconds
    time.sleep(2)

    # Assign and declare a variable to represent the html object
    htmlMarsWeather = browser.html

    # Parse htmlMarsWeather with bs
    parsed_htmlMarsWeather = bs(htmlMarsWeather, 'html.parser')

    # Find all new weather tweets 
    newWeatherTweets = parsed_htmlMarsWeather.find('div',class_ ="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

    # Scrape for div and span
    tweets = newWeatherTweets.find('span', class_ ="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    weather = tweets.text
    print(weather)

    # Save MARS weather
    scraped_data['weather'] = weather
    

    marsFacts = "https://space-facts.com/mars/"
    pd_table = pd.read_html(marsFacts)
    a = pd_table[0]
    a.columns = ["Measurements", "value"]

    # Declare and assign a variable to store the data from a and the html from 
    # which it came
    df = a.to_html(classes = 'table table-striped')
    
    # Save facts
     scraped_data['facts'] = df
        
    # Declare and assign a variable to store the data from a and the html from 
    # which it came
    df = a.to_html(classes = 'table table-striped')
        
     # Declare and assign a variable to be the hemis url
    hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    
    # Go to hemis website via splinter
    browser.visit(hemi)

    # Use time.sleep function to slowdown execution by two seconds
    time.sleep(2)

    # Assign and declare a variable to represent the html object
    html_hemis = browser.html

    # Use bs to parse html_hemis
    p_parse = bs(html_hemis, "html.parser")

    # Parse further to isolate the item class (use find_all because we're working toward getting all images)
    items= p_parse.find_all("div", class_="item")


    # Commence a empty list to store the images' urls
hemis_urls = []

# Create and assign a variable to be the the index's url
index_url = "https://astrogeology.usgs.gov"

# Commence a for loop to loop through the data in df variable
for i in items:
    # Declare and assign a variable to hold the titles related to the hemi images
    # Note that the data does not have a class because it is a header div
    hemi_title = i.find("h3").text
        
    # Declare and assign a variable to store the thumb-nail image
    thumb = i.find("a", class_="itemLink product-item")["href"]
    
    # Go to the urls of the large images, which consist of the htmls hemis' wevsites
    # and the html of the thumb
    browser.visit(index_url + thumb)
    
    # Assign and declare a variable to represent the html object of the thumbs
    thumb = browser.html
    
    # Utilize bs to parse the html stored in the thumb_url variable
    fresh_soup = bs(thumb, "html.parser")
    time.sleep(3)


    # Create and assign a variable to represent the url of the large image found in the img tag and has a class of wide-image
    wideImage = index_url + fresh_soup.find("img", class_="wide-image")["src"]
    
    # Utilize .append to create an array of objects that are dicts. Store in empty list
    hemis_urls.append({"title": title, "url":wideImage})
    
    # Save image urls

    scraped_data['mars_hemispheres'] = hemis_urls

    browser.quit()
    return scraped_data
    
    