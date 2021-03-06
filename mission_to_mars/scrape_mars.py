#import dependencies
from bs4 import BeautifulSoup
import requests
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

## define scrape funciton
def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_collection={}
    
    #Mars news scraping
    url = 'https://redplanetscience.com'
    browser.visit(url)
    time.sleep(2)    
    # create html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('section', class_='image_and_description_container')
    queries = results.find_all('div', class_='col-md-12')
    
    #create lists for news title and texts
    news_heading = []
    news = []
    
    
    for query in queries:
        heading = query.find('div', class_='content_title').text
        news_text = query.find('div', class_='article_teaser_body').text
        news_heading.append(heading)
        news.append(news_text)
        
        
    mars_collection["News_Heading"] = news_heading
    mars_collection["News_Text"] = news
    
    #Mars space Featured image
    
    # use url to get html
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    
    #use splinter to click to hte full image link
    browser.links.find_by_partial_text('FULL IMAGE').click()
    
    # create beautiful soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #finding link for the image
    header = soup.find('div', class_='header')
    result = header.find('div', class_='floating_text_area')
    link = result.find('a')
    href = link['href']
    full_link = url +'/'+ href
    
    mars_collection["Featured_Image"] = full_link
    
    
    ##Mars facts
    #Pandas read html
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    #pandas dataframe
    facts_df = tables[0]
    # dataframe to html
    facts_html = facts_df.to_html()
    html_table=facts_html.replace("\n", "")
    
    mars_collection["Facts"] = html_table
    
    ## Mars Hemisphere
    # creating dictionary for hemisphere images
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html

    #create dictionary list with hemisphere names and the corresponding image links
    image_list = []
    hemispheres = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced", 
                   "Syrtis Major Hemisphere Enhanced","Valles Marineris Hemisphere Enhanced"]
    for hemisphere in hemispheres:
        html = browser.html
        browser.links.find_by_partial_text(hemisphere).click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('div', class_='downloads')
        image = result.find_all('li')
        link = image[0]
        a_tag = link.find('a')
        href = a_tag['href']
        full_url = url+href
        dict = {"title": hemisphere, "image_url": full_url}
        image_list.append(dict)
        browser.links.find_by_partial_text("Back").click()

    
    mars_collection["Hemispheres"] = image_list
    browser.quit()
    
    return mars_collection
    
    
    
    
