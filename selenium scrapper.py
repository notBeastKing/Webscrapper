import os
import time
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
Base_URL = "https://www.flipkart.com"

# Function to go to product review page from the main product page
def go_to_reviewpage(URL):
    Review_link = ''
    driver.get(URL)  # sending a get request to the main page URL
    time.sleep(2)  # wait for page to laod
    main_page = BeautifulSoup(driver.page_source, 'html.parser')  # formatting the HTML code
    all_reviews_div = main_page.find_all("div", attrs={"class": "col pPAw9M"})  # finding column "col pPAw9M" which has the href link to all reviews

    # finding the product review link
    for a in all_reviews_div:  # looping through all the div tags that have class "col pPAw9M"
        for href in a:  # looping through all the tags under the div tag with class "col pPAw9M" to find the href link
            if href.get("href") is not None:  # there are multiple a tags under "col pPAw9M"; only 1 a tag with href has the link we want (for product reviews)
                Review_link = href.get("href")  # storing that link

    print('Entered review')
    all_reviews_link = Base_URL + Review_link  # creating the link by attaching the base URL to Flipkart to it
    print(all_reviews_link)

    driver.get(all_reviews_link)  # navigating to the review page
    time.sleep(2)  # waiting for the page to load
    review_page = BeautifulSoup(driver.page_source, 'html.parser')  # formatting the HTML

    return review_page

# Function to request HTML code from link
def get_html(URL):
    url_temp = Base_URL + URL
    driver.get(url_temp)
    time.sleep(2)  # waiting for the page to load
    temp_page = BeautifulSoup(driver.page_source, 'html.parser')
    return temp_page

# Function to scrape reviews
def Scrape(main_URL):
    review_page = go_to_reviewpage(main_URL)
    overall_rating = review_page.find_all("div", attrs={"class": "ipqd2A"})  # getting the overall rating of the product in the div tag with class "ipqd2A"
    for rating in overall_rating:
        print(rating.text)  # since it's in a list, we only need the first element

    reviews = []
    find_next = review_page.findAll("a", attrs={"class": "_9QVEpD"}, string="Next")  # seeing if the next link exists on the page
    next_link = ''
    i = 0
    while find_next:  # a loop to go to all the pages and get reviews
        print(i, "\n")
        if i > 15:
            break
        print("\n entered thingy \n")
        all_reviews = review_page.find_all("div", attrs={"class": "ZmyHeo"})  # all reviews are under the div tag and class ZmyHeo
        for review in all_reviews:
            reviews.append(review.text)

        find_next = review_page.find_all("a", attrs={"class": "_9QVEpD"}, string="Next")  # find the next link to go to the next page of reviews
        for link in find_next:
            if link.get("href") is not None:
                next_link = link.get("href")
        review_page = get_html(next_link)
        i += 1
    print(len(reviews))
    print("\n")
    for review in reviews:
        print(review, "\n")

    return reviews

Scrape("https://www.flipkart.com/apple-iphone-15-green-128-gb/p/itm235cd318bde73?pid=MOBGTAGPYYWZRUJX&lid=LSTMOBGTAGPYYWZRUJXUGY7PM&marketplace=FLIPKART&q=iphone+&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=b1e52a41-054e-4ca3-ac02-fe5306d61ead.MOBGTAGPYYWZRUJX.SEARCH&ppt=hp&ppn=homepage")
