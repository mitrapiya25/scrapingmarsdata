
# coding: utf-8

# In[34]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import pymongo


# In[2]:

def scrape():
    executable_path = {'executable_path': 'C:\\Users\\mitra\\chromedriver_win32\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


# In[4]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


# In[5]:


    title =soup.find("div", class_ = "content_title")
    para= soup.find("div",class_ = "article_teaser_body")


# In[6]:


    news_title = title.text


# In[7]:


    news_para = para.text
    
    scraped_data = {}
    scraped_data["News_title"] = news_title
    scraped_data["New_para"] = news_para


# In[9]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    mars_browser=browser.html
    mars_soup = BeautifulSoup(mars_browser, 'html.parser')


# In[29]:


    image = mars_soup.find("div",class_="img")
    featured_image_url = (image.find("img"))['src']
    base = "https://www.jpl.nasa.gov/"
    featured_image_url = urljoin(base, featured_image_url)

    scraped_data["Image_URL"] = featured_image_url
# In[30]:


    

# In[31]:


    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    mars_tweet=browser.html
    mars_tweet_soup = BeautifulSoup(mars_tweet, 'html.parser')


# In[33]:


    mars_wether = mars_tweet_soup.find("div", class_="js-tweet-text-container").p.text

    scraped_data["Mars_weather"]=mars_wether
# In[35]:


    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    tables


# In[40]:


    mars_fact_df = tables[0]
    mars_fact_df.columns = ["Attributes","Values"]


# In[44]:


    mars_fact_df
    html_table = mars_fact_df.to_html()
    html_table = html_table.replace('\n', '')
    mars_fact_dict_df_1 = mars_fact_df.set_index("Attributes").to_dict("dict")
    scraped_data["Mars_Fact"] = mars_fact_dict_df_1["Values"]
    # In[86]:


    titles=[]
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    geology = browser.html
    geology_soup = BeautifulSoup(geology, 'html.parser')
    description = geology_soup.find_all("div",class_="description") 
    for desc in description:
        titles.append(desc.a.h3.text)
    
# In[87]:


    images = []
    for i in range(4):
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        browser.click_link_by_partial_text(titles[i])
        image = browser.html
        image_soup = BeautifulSoup(image, 'html.parser')
        image_download = (image_soup.find("div", class_="downloads")).ul
        for image in image_download.find_all("li"):
            image_1 = image.find("a")
            if image_1.text == "Sample":
        ##print(image.find("a")["href"])
                images.append({"image_title":titles[i] ,"image_url": image_1["href"]})
    scraped_data["Images"] = images 
    print(scraped_data)      
    return(scraped_data)        




