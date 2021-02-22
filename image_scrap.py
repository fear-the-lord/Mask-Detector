# Import the necessary dependencies
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import sys
import os

# Providing the keyword that we want to search
download = 'face images'
# Create the URL
site = 'https://www.google.com/search?tbm=isch&q=' + download


# Providing path to the mozilla driver
driver = webdriver.Firefox(executable_path = 'C:/Users/admin/Desktop/Mask Detector/driver/geckodriver.exe')

# Passing site URL
driver.get(site)
# Below while loop scrolls the webpage 10 times (if available)
i = 0
while i < 10:  
    # For scrolling page
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    try:
        # For clicking 'show more results' button
        driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[5]/input").click()
    # Handle exceptions
    except Exception as e:
        pass
    # Wait for sometime, after every scroll
    time.sleep(5)
    i += 1

# Parse the page
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Closing web browser
driver.close()

# Scraping image urls with the help of image tag and class used for images
img_tags = soup.find_all("img", class_ = "rg_i")
# To count the number of images downloaded
count = 0
for i in img_tags:
    try:
        # Passing image urls one by one and downloading and storing it the required folder
        filepath = 'dataset/without_mask/' + str(count) + ".jpg"
        urllib.request.urlretrieve(i['src'], filepath)
        count += 1
        print("Number of images downloaded = "+str(count), end = '\r')
    # Handle exceptions
    except Exception as e:
        pass
print("[INFO] Images Downloaded Successfully...")
