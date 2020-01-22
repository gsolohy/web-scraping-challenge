import pandas as pd

import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

import pymongo

def init_browser():
    # Execute chromedriver.exe
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # NASA Mars News
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(2)

    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'lxml')

    first_article = nasa_soup.find('div',class_="list_text")
    news_date = first_article.find('div', class_="list_date").text
    news_title = first_article.find('div', class_="content_title").text
    news_p = first_article.find('div',class_="article_teaser_body").text

    print(f"Date: {news_date} \nTitle: {news_title} \nParagraph: {news_p}")

    
    # JPL Mars Space Images - Featured Image
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')

    current_href = img_soup.find('a', class_="button fancybox")['data-fancybox-href']
    featured_image_url = f'https://www.jpl.nasa.gov{current_href}'
    
    print(f'Featured Image_url: {featured_image_url}')
    
    
    # Mars Weather
    twiiter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twiiter_url)
    time.sleep(2)

    wthr_html = browser.html
    wthr_soup = bs(wthr_html, 'lxml')

    # wthr_xpath = '//*[@id="stream-item-tweet-1207720064440553478"]/div[1]/div[2]/div[2]/p'
    xpath2 = '/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[2]/div[1]/div[2]/div[2]/p'
    # mars_weather = browser.find_by_xpath(wthr_xpath).text
    mars_weather = browser.find_by_xpath(xpath2).text
    print(f'Mars Weather: {mars_weather}')

    
    # Mars Facts
    fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)
    browser.visit(fact_url)
    time.sleep(2)

    mars_fact = tables[1]
    del mars_fact['Earth']
    mars_fact.rename(columns={'Mars - Earth Comparison':'Description'}, inplace=True)
    mars_fact.set_index('Description', inplace=True)
    mars_fact_html = mars_fact.to_html()
    
    
    # Mars Hemispheres
    atro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(atro_url)
    time.sleep(2)

    products_html = browser.html
    products_soup = bs(products_html, 'lxml')
    products_items = products_soup.find_all('div', class_='item')

    visit_urls = []
    for i in products_items:
        link_url = i.find('a', class_="itemLink product-item")['href']
        visit_urls.append(link_url)
        time.sleep(2)

    baseURL = 'https://astrogeology.usgs.gov'
    titles = []
    img_url = []
    for visit in visit_urls:
        search_url = baseURL+visit
        browser.visit(search_url)
        time.sleep(2)
        hem_html = browser.html
        hemi_soup = bs(hem_html, 'lxml')
        
        hemi_url = hemi_soup.find('img', class_="wide-image")['src']
        img_url.append(baseURL+hemi_url)
        
        hemi_title = hemi_soup.find('h2',class_="title").text
        titles.append(hemi_title)

    hemisphere_image_urls = []
    for i in range(4):
        hemisphere_image_urls.append({'title': titles[i], 'img_url': img_url[i]})
    print(hemisphere_image_urls)

    browser.quit()
    print('Scrape Completed')
    
    # MongoDB Mars Data in dictionary
    mars_data = {'news_date': news_date,
                 'news_title': news_title,
                 'news_p': news_p,
                 'featured_image_url': featured_image_url,
                 'mars_weather': mars_weather,
                 'mars_fact_html': mars_fact_html,
                 'hemisphere_image_urls': hemisphere_image_urls}
    
    return mars_data