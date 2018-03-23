# Download: lxml, selenium, requests, time, chromedriver, playsound
from lxml import html
import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from playsound import playsound

# A constant for how many loops I will allow for with the same url.
MAX_LOOPS = 2
# A constant of how many seconds we are willing to let the page load before trying again.
# We set this to '0' and put a continue for the TimeoutException so that we will never
# progress until we load the price-container.
WAIT_TIME = 0
# Part of html we need to load before scanning for price
HTML_CLASS_NAME = 'showAll--container'

# This is the url I want us to start at.
starter_url = 'https://bookscouter.com/sell/0811866572-slow-cooker-the-best-cookbook-ever-with-more-than-400-easy-t'

# This will open up a Chrome browser.
driver = webdriver.Chrome()
driver.get(starter_url)

# This tells us if the book is worth something. There is another
# identifier if it's not able to be sold.
worth_money = '<div class="price__child price__price flex-child__auto">'
price_class = 'a.link--sell.btn.action'
#vendor_class = 'a.action.showReviews'

# Making a null variable to keep track of the previous url.
prev_url = None

while 1:
    # This is subject to change. We might want to get rid of it entirely and
    # just worry about MAX_LOOPS. It depends on the internet connection.
    # For this we will need to test it a lot in the real conditions.
    # This value should always be greater than or equal to twice the time
    # it takes to load a webpage.
    #time.sleep(WAIT_TIME);
    curr_url = driver.current_url
    if curr_url != prev_url:
        try:
            myElement = WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.CLASS_NAME, HTML_CLASS_NAME)))
        except TimeoutException:
            continue
        # I can run through each "worth_money" entry by using for .. in ..but idk if there is a way
        # to match it to its respective Data-Name (ie name of vendor)
       # if worth_money in driver.page_source:
       #     if count < MAX_LOOPS:
       #         playsound('bell.wav')
       # else:
       #     if count < MAX_LOOPS:
       #         playsound('plop.wav')
        prev_url = curr_url

        prices = driver.find_elements(By.CSS_SELECTOR, price_class)
        # We start at the second index because there is a duplicate at the beginning caused
        # by the site posting the best offer in two places, whereas every other price is
        # only posted once.
        for price in prices[1::]:
            print(price.get_attribute('data-vendor'), price.get_attribute('data-price'))
