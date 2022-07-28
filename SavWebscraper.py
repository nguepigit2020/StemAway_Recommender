"My complete webscraper"
"Example webpage https://forums.gearboxsoftware.com/c/borderlands-3/borderlands-3-news/247"
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import requests, os, time
import pandas as pd
import numpy as np
import regex as re

"""
Class structure
init
main -> runScraper
runScraper -> getLinks
getLinks -> scroll -> then returns links

"""
"""
TODO: Ensure leading posts are imported correctly
TODO: Add functions to collect other features (Replies, Views, Number of replies, tags)
"""

class webScrape:

    browser= None
    PostDict= {}
    PostDf= pd.DataFrame(columns= [
        'Post_Title',
        'Leading_Post',
        'Date_Created'
    ])

    def __init__(self):
        #Set up webdriver
        opts = Options()
        opts.add_argument('--headless')
        opts.add_argument('--incognito')
        self.driver= webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=opts)

    #Scrolls through the webpage
    def scroll(driver, timeout):
        scroll_pause_time= timeout

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # Load the entire webage by scrolling to the bottom
        lastHeight = driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        while (True):
            # Scroll to bottom of page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for new page segment to load
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break

            lastHeight = newHeight

    #Getting the title of the post
    def getTitle(Topicsoup):
        soup= Topicsoup
        Title= soup.find('title').text

        if Title is None:
            Title= 'No Title'

        return Title

    #Getting the Leading post of the post
    def getLeadingPost(Topicsoup):
        LeadingPost= Topicsoup.div.find(class_='post').text

        if LeadingPost is None:
            LeadingPost = str(0)

        return LeadingPost

    #Getting the dates created
    def getDateCreated(Topicsoup):
        DateCreated= soup.div.find('time', class_='post-time').text

        if DateCreated is None:
            DateCreated = str(0)

        return DateCreated

    # Getting the links
    def getLinks(self, url):
        #waiting for page to load
        driver.implicitly_wait(30)
        #getting driver to open link
        driver.get(url)
        #using scroll function to scroll to the bottom
        scroll(driver, 2)
        #Getting html from entire webpage
        Bsoup= BeautifulSoup(driver.page_source, 'lxml')
        #closing driver
        driver.close()

        #List to store the links we will get
        Links=[]

        #Getting all the links in the webpage
        for link in Bsoup.find_all('a', class_='title raw-link raw-topic-link'):
            Links.append(link['href'])

        return Links

    def runScraper(self, SiteName):

        Links= webScrape.getLinks('https://forums.gearboxsoftware.com/c/borderlands-3/borderlands-3-news/247')

        for link in Links:
            #Opens the links as they come as parts on the webpage
            self.driver.get('https://forums.gearboxsoftware.com'+link)
            #Page HTML stored in PHTML
            PHTML= self.driver.page_source
            #Page Soup stored in PSoup
            PSoup= BeautifulSoup(PHTML, 'html.parser')

            #Getting data from the pages
            Post_Title= self.getTitle(PSoup)
            Leading_Post= self.getLeadingPost(PSoup)
            Date_Created= self.getDateCreated(PSoup)

            #Attribute dictionary where we'll temporarily store the data we collect
            attributeDict= {
                'Post_Title': Post_Title,
                'Leading_Comment': Leading_Post,
                'Date_Created': Date_Created
            }
            self.PostDict[Post_Title]= attributeDict
            self.PostDf= self.PostDf.append(attributeDict, ignore_index= True)

            #Testing
            print('Title: ', Post_Title)
            print('Leading Post', Leading_Post)
            print('Date of Creation', Date_Created)

        #Getting timestamp
        timeStamp = datetime.now().strftime('%Y%m%d')

        #Setting up csv file
        "Please put your name here"
        csvFilename = 'NameHere' + '_SCRAPED_DATA' + timeStamp + '.csv'
        csvFileFullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), csvFilename)
        # Save dataframe into csv file
        self.topic_df.to_csv(csvFileFullPath)

if __name__ =='__main__':
    #Local path to the webdriver
    #webdriverPath = r'C:\Users\savan\Desktop\Coding and Software\Stemaway Coding Stuff\chromedriver.exe'
    
    # Forum to scrape URL    
    BaseURL = 'https://forums.gearboxsoftware.com/c/borderlands-3/borderlands-3-news/247'
    
    # Name of the forum
    SiteName = 'Boarderlands'
        
    # WebScraping object
    webScrape = webScrape()
    
    # Run the webscraper and save scraped data
    webScrape.runScraper(SiteName)
        
