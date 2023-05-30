#! Don't run this at work!

import pdb

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_driver_path = f"{os.environ.get('CHROME_DRIVER_PATH')}/chromedriver.exe"

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "http://orteil.dashnet.org/experiments/cookie/"
driver.get(url)
driver.set_window_position(-2568, -722)

#LOCATORS
cookie = driver.find_element(By.ID, "cookie")
while True:
    cookie.click()



