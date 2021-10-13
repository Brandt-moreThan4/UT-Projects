"""Script to scrape edmunds forum comments."""


from typing import Text
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd


def get_chrome_driver():
    """Returns a selenium driver object to manipulate chrome"""

    driver_path = r'C:\Users\User\OneDrive\Desktop\chromedriver.exe'
    options = webdriver.chrome.options.Options()
    options.set_headless(headless=False)
    try:
        driver = webdriver.Chrome(driver_path, options = options)
    except:
        print('Something screwed up getting the driver. Make sure chrome is downloaded and the path is correct')
        return None
    else:
        return driver


desired_comments = 5000
driver = get_chrome_driver()

next_url = 'https://forums.edmunds.com/discussion/2864/general/x/entry-level-luxury-performance-sedans'

all_comments = []
while True:
    driver.get(next_url)
    time.sleep(8) # I think you need to sleep for awhile to let all the javascript load.
    html = driver.page_source # Get the html
    soup = BeautifulSoup(html) # make some easy to slurp soup

    comments = soup.find_all('li', class_='ItemComment')
    
    for comment in comments:
        comment_date = comment.find(class_='DateCreated').text.strip()
        comment_text = comment.find('div',class_='Item-BodyWrap').text.strip()

        comment_username = comment.find(class_='Author').text.strip()
        comment_post_count = comment.find(class_='PostCount').text.strip()

        all_comments.append([comment_date,comment_text,comment_username,comment_post_count])

    # If we have enough comments then exit the loop. Otherwise get, the next page and continue
    if len(all_comments) >= 5000:
        break
    else:
        next_url = soup.find('a', class_='Next')['href']
        # print(next_url)




df = pd.DataFrame(data=all_comments,columns=['date','text','username','post_count'])
df.to_csv('assignment_1/edmunds.csv',index=False)
