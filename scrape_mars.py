from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

mars_info={}

def scrape_data():
    try:
        # Scrape latest news
        browser=init_browser()
        news_url="https://mars.nasa.gov/news/"

        browser.visit(news_url)
        
        html=browser.html
        soup=BeautifulSoup(html, 'html.parser')

        news_title=soup.find('div', class_='content_title').find('a').text
        news_p=soup.find('div', class_='article_teaser_body').text
        news_url=soup.find('div', class_='content_title').find('a')['href']

        mars_info["news_title"]=news_title
        mars_info['news_paragraph']=news_p
        mars_info['news_url']=news_url

        # scraping Mars featured image.
        image_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

        browser.visit(image_url)

        html_image=browser.html
        soup=BeautifulSoup(html_image, 'html.parser')
        main_url='https://www.jpl.nasa.gov/'

        response=soup.find('article')['style']
        response=response.replace('background-image: url(',"").replace(');','')
        response=response[2:-1]
        featured_image=main_url+response
        
        image_title=soup.find('h1', class_="media_feature_title").text
        mars_info["featured_image"]=featured_image
        mars_info["image_title"]=image_title

        #scraping Mars Weather
        weather_url="https://twitter.com/marswxreport?lang=en"

        browser.visit(weather_url)

        weather=browser.html
        soup=BeautifulSoup(weather, 'html.parser')

        mars_weather=soup.find('p', class_='js-tweet-text').text
        mars_info["weather"]=mars_weather

        #scraping Mars Facts
        facts_url="https://space-facts.com/mars/"

        browser.visit(facts_url)

        tables = pd.read_html(facts_url)
        facts=tables[0]
        facts.drop('Earth', axis=1, inplace=True)
        facts.columns=['Description',"Value"]
        facts.set_index('Description', inplace=True)

        facts_html=facts.to_html()

        mars_info['mars_facts']=facts_html

        #scrapping Hemispheres
        hemisphere_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

        browser.visit(hemisphere_url)

        hemisphere=browser.html
        soup=BeautifulSoup(hemisphere, 'html.parser')
        results=soup.find_all('div', class_="item")

        Hemisphere_image_urls=[]

        main='https://astrogeology.usgs.gov'

        for result in results:
            title=result.find('h3').text
            partial_url=result.find('div', class_='description').find('a')['href']
            
            imagePage_url=main+partial_url
            browser.visit(imagePage_url)
            image_loc=browser.html
            
            image_info=BeautifulSoup(image_loc, 'html.parser')
            
            img_url=image_info.find('img', class_='wide-image')['src']
            img_url=main+img_url
            
            image={
                'title': title,
                'img_url': img_url
            }
            
            Hemisphere_image_urls.append(image)

        mars_info['hemispheres']=Hemisphere_image_urls

        return mars_info
    finally:
        browser.quit()