import requests
from bs4 import BeautifulSoup
import time

#global variables
Base_URL = "https://www.flipkart.com"

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }  # WE use these headers to make it seem like this get request is coming from an actual web browser 

#function to go to product review page from main product page
def go_to_reviewpage(URL):
    Review_link = ''
    main_page_temp = requests.get(URL,headers=headers) #sending a get request to the main page url 
    time.sleep(3)
    print(main_page_temp)
    main_page = BeautifulSoup(main_page_temp.content,'html.parser') #formatting the html code
    all_reviews_div = main_page.find_all("div",attrs={"class":"col pPAw9M"})#finding colum "col pPAw9M" which has the href link to all reviews 

    #finding the product reivew link

    for a in all_reviews_div:   #looping through all the div tags that have class "col pPAw9M"
        for href in a:          #looping through all the tags under the div tag with class "col pPAw9M" to find the href link
          if href.get("href") != None:      #there are multiple a tags under "col pPAw9M" however there is only 1 a tag with href and that has the link we want(for product reviews) 
             Review_link = href.get("href")  #we are storing that link in

    print('Entered review')
    all_reviews_link = Base_URL+Review_link #creating the link by attaching the base url to flipkart to it 
    print(all_reviews_link)

    review_page_temp = requests.get(all_reviews_link,headers=headers) #requesting Review page html
    review_page = BeautifulSoup(review_page_temp.content,'html.parser') #formating the html

    return review_page

#fucntion to request html code form link
def get_html(URL):
    url_temp = Base_URL+URL
    temp = requests.get(url_temp,headers=headers)
    temp_page = BeautifulSoup(temp.content,'html.parser')
    return temp_page
   
#function to scrape reviews
def Scrape(main_URL):
    review_page = go_to_reviewpage(main_URL)
    overall_rating = review_page.find_all("div",attrs={"class":"ipqd2A"}) #getting the overall rating of the product its given in the div tag with class "ipqd2A" 
    for rating in overall_rating:
        print(rating.text) #since its in a list we only need the first element of it 

    reviews = []
    find_next = review_page.findAll("a",attrs={"class":"_9QVEpD"},string="Next") #seeing if the next link exists on the page
    next_link = ''
    i = 0
    while(find_next != []): #a loop to go to all the pages and get reviews
        print(i,"\n")
        if i > 15:
            break
        print("\n entered thingy \n")
        all_reviews = review_page.find_all("div",attrs={"class":"ZmyHeo"}) #all reviews are under the div tag and class ZmyHeo
        for review in all_reviews:
            reviews.append(review.text)

        find_next = review_page.find_all("a",attrs={"class":"_9QVEpD"},string="Next")#find the next link to go to the next page of reviews
        for link in find_next:
            if link.get("href") != None:
                next_link = link.get("href")
        review_page = get_html(next_link)    
        i += 1
    print(len(reviews)) 
        
    return reviews

    
reviews = Scrape("https://www.flipkart.com/apple-iphone-15-green-128-gb/p/itm235cd318bde73?pid=MOBGTAGPYYWZRUJX&lid=LSTMOBGTAGPYYWZRUJXUGY7PM&marketplace=FLIPKART&q=iphone+&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=b1e52a41-054e-4ca3-ac02-fe5306d61ead.MOBGTAGPYYWZRUJX.SEARCH&ppt=hp&ppn=homepage&ssid=gslh00aalb103egw1719898972869&qH=4673a7c42221208f")

for review in reviews:
    print(review,"\n")
