# Python program to download comics from multiple different websites
# using Selenium and Requests, through XPath and WebScraping

# Import modules
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import sys

# Start function to open browser in Incognito Mode
def start(url):
    # Open Chrome Browser in INcognito Mode
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--start-minimized")
    browser = webdriver.Chrome(options = chrome_options)

    # Hide browser without minimizing
    # Note: browser.minimize_window() will cause program to stop going to next page
    # browser.set_window_position(-10000, 0)

    browser.get(url)

    return browser

# Input method to recieve input from user
def recieveInput():
    # input comic URL of 1st page
    while True:
        url = input('Comic URL: ')

        try:
            requests.get(url)
            break
        except requests.exceptions.MissingSchema:
            print("Invalid URL")
        except requests.ConnectionError:
            print("Invalid URL")

    # Clear Terminal when downloading a new comic
    os.system('cls')

    # print(f'Comic URL: {url}')

    # # input comic name
    # name = input('Comic Name: ').replace(':', ' -')
    # Length of comic for Loop
    #comicLength = int(input('Amount of pages: '))

    return url #, name

def get_title(browser, title_path):
    title = browser.find_element(By.XPATH, title_path).text
    return title

# Function to create new folder to store comic
def makeFolder(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print(f'{name} already exists')

# Method to check which website the comic coes from
def comicSourceSite(url):
    #print(' ')

    # Dictionary with comic Source for XPath and image_class
    comicSources = {
        "ReadComicsOnline.ru  -> ": 1,
    }
    # To add other sites, simply add new Option in Dictionary
    # and in IF Elif add new with nextButtonXPath and Image Tag for site

    # Comic Source
    if 'readcomicsonline' in url:
        source = 1

    # Chooses nextButtonXPath, title XPATH and img class name depending on comic source
    match (source):
        case 1:
            nextButtonXPath = '/html/body/div[3]/div[1]/div/div/div[3]/ul[2]/li/a'
            image_class = 'scan-page'
            title_path = '/html/body/div[3]/div[1]/div/div/div[1]/a'

        case _:
            print('Invalid source. Closing program')
            exit()

    return nextButtonXPath, image_class, title_path

# Function to download images
def downloadImages(browser, image_class, title_path, nextButtonXPath):
    browser.implicitly_wait(3)

    prev_url = ''
    prev_name = ''

    while True:
        # Reset page counter
        j = 1

        name = get_title(browser, title_path)

        if name != prev_name:
            makeFolder(name)
            prev_name = name

        # Loop pages of current issue
        while True:
            # Get title
            name = get_title(browser, title_path)

            # Get current URL
            imageURL = browser.find_element(By.CLASS_NAME, image_class).get_attribute('src')

            # If imageURL is same as prev, comic is done. If name is not same, Issue is done
            if imageURL == prev_url or name != prev_name:
                print('Finished Issue')
                break

            # Get image
            r = requests.get(imageURL)

            # Save current page
            with open(f'{name}/{name} pg{j}.png', 'wb') as f:
                print("\rSaving pg{}".format(j), end='')
                f.write(r.content)

            # Update page counter
            j+=1

            prev_url = imageURL

            nextButton = browser.find_element(By.XPATH, nextButtonXPath)
            nextButton.click()
            browser.implicitly_wait(3)

        if imageURL == prev_url:
            print('Finished Comic!')
            break


# Run method to run program
def run():

    # Recieves data from Input method
    url = recieveInput()

    # Obtain XPath for Next button and Image Tag and Title Xpath from source
    nextButtonXPath, image_class, title_path = comicSourceSite(url)

    # Open Browser
    browser = start(url)

    # Minimize browser after starting it
    browser.minimize_window()

    # Calls function to download images
    downloadImages(browser, image_class, title_path, nextButtonXPath)

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

    # Clear Terminal
    os.system('cls' if os.name == 'nt' else 'clear')