# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import pymongo


executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape_all():
    browser = Browser('chrome', **executable_path, headless=True)
    url= "https://redplanetscience.com/"
    browser.visit(url)
    soup=bs(browser.html,'html.parser')

    title=soup.find('div', class_="content_title").text
    para = soup.find('div', class_="article_teaser_body").text

    url= "https://spaceimages-mars.com"
    browser.visit(url)
    soup = bs(browser.html,'html.parser')

    truncated_url=soup.find('img', class_="headerimage")["src"]
    featured_img_url=f"{url}/{truncated_url}"
    
    url= "https://galaxyfacts-mars.com"
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.columns=df.iloc[0]
    df=df[1:]
    df.set_index(df.columns[0])
    td= df.to_html()

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    soup=bs(browser.html, 'html.parser')

    h3=soup.find_all('h3')
    four_h3= [tag.text for tag in h3][:-1]

    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item img')
    for i in range(len(links)):
        hemisphere = {}
    
        browser.find_by_css('a.product-item img')[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    data = {
        "title":title,
        "paragraph":para,
        "featured_img":featured_img_url,
        "mars_facts":td,
        "hemisphere":hemisphere_image_urls
    }

    browser.quit()

    return data
