# Python program to download comics from multiple different websites 
# using Selenium and Requests, through XPath and WebScraping

# Import modules
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import sys

# Start function to open browser in Incognito Mode
def start(url):
    # Open Chrome Browser in INcognito Mode
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    browser = webdriver.Chrome(chrome_options = chrome_options)

    browser.get(url)

    return browser

# Input method to recieve input from user
def recieveInput():
    # input comic URL of 1st page
    url = input('Comic URL: ')
    # input comic name
    name = input('Comic Name: ')
    # Length of comic for Loop
    comicLength = int(input('Amount of pages: '))

    return url, name, comicLength

# Function to create new folder to store comic
def makeFolder(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print(f'{name} already exists')

# Method to check which website the comic coes from
def comicSourceSite():
    print(' ')

    # Dictionary with comic Source for XPath and imageTag
    comicSources = {
        "ReadComicsOnline -> ": 1
        # Add new options to the menu so more sites can be scraped
    }
    # To add other sites, simply add new Option in Dictionary 
    # and in IF Elif add new with nextButtonXPath and Image Tag for site

    print(' ')
    # Print dictionary so user can input comic source site
    for source, option in comicSources.items():
        print(source, option)
    
    # User inputs Comic Source site
    source = int(input('Comic Source Site: '))

    # Chooses nextButtonXPath and image HTML tag depending on comic source
    if source == 1:
        nextButtonXPath = '/html/body/div[3]/div[1]/div/div/div[3]/ul[2]/li/a'
        imageTag = 'img.img-responsive.scan-page'
    # Add new if, elif statements where the XPath for the next button and the image tag are set.
    else:
        print('Invalid source. Exiting program')
        exit()
    
    return nextButtonXPath, imageTag

# Function to download images
def downloadImages(browser, imageTag, name, nextButtonXPath,comicLength):
    browser.implicitly_wait(3)

    # Loop to iterate through comic pages
    for i in range(comicLength):
        j = i+1

        # Obtain image source URL to download by finding elements that match image tag
        imageURL = browser.find_element_by_tag_name(imageTag).get_attribute('src')

        # Sends request with source imageURL to recieve image
        r = requests.get(imageURL)

        # Saves image to desired folder
        with open(f'{name}/{name} pg{j}.png', 'wb') as f:
                    f.write(r.content)

        # Finds Next button on comic to go to next page
        nextButton = browser.find_element_by_xpath(nextButtonXPath)

        # Clicks next button to go to next page
        nextButton.click()
        browser.implicitly_wait(3)

# Run method to run program
def run():

    # Recieves data from Input method
    url, name, comicLength = recieveInput()

    # Obtain XPath for Next button and Image Tag from source
    nextButtonXPath, imageTag = comicSourceSite()

    # Creates folder to store comic
    makeFolder(name)
    
    # Calls function to start browser
    browser = start(url)
    
    # Minimize browser after starting it
    browser.minimize_window()
    
    # Calls function to download images
    downloadImages(browser, imageTag, name, nextButtonXPath, comicLength)

    # Quit browser after comic is downloaded
    browser.quit()

# Loop to download multiple comics until user decides to stop
next = True
while next == True:
    run()
    print('')
    again = input('Download another comic? y/n: ')

    if again == 'n':
        break
