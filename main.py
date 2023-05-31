#! Don't run this at work!  Or do short durations
# 0.1251|16650|26|228|23|942|20|3384|17|10123|14|26600|11|142667|0|1000000|0|123456789
import pdb

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

path = "C:/Users/Christopher/drivers/chromedriver.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_driver_path = path

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "http://orteil.dashnet.org/experiments/cookie/"
driver.get(url)

# LOCATORS
cookie = driver.find_element(By.ID, "cookie")
upgrades = driver.find_elements(By.CSS_SELECTOR, "#store div")
upgrade_ids = [item.get_attribute("id") for item in upgrades]
# for upgrade in upgrades:
#     upgrade_ids.append(upgrade.get_attribute("id"))

# Get upgrade item ids.
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

PAUSE_TIMER = time.time() + 5
END_TIMER = time.time() + 60 * 5  # 5minutes


def working_code(timeout, five_min):
    while True:
        cookie.click()

        # Every 5 seconds:
        if time.time() > timeout:

            # Get all upgrade <b> tags
            all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
            item_prices = []

            # Convert <b> text into an integer price.
            for price in all_prices:
                element_text = price.text
                if element_text != "":
                    cost = int(element_text.split("-")[1].strip().replace(",", ""))
                    item_prices.append(cost)

            # Create dictionary of store items and prices
            cookie_upgrades = {}
            for n in range(len(item_prices)):
                cookie_upgrades[item_prices[n]] = item_ids[n]

            # Get current cookie count
            money_element = driver.find_element(By.ID, "money").text
            if "," in money_element:
                money_element = money_element.replace(",", "")
            cookie_count = int(money_element)

            # Find upgrades that we can currently afford
            affordable_upgrades = {}
            for cost, id in cookie_upgrades.items():
                if cookie_count > cost:
                    affordable_upgrades[cost] = id

            # Purchase the most expensive affordable upgrade
            highest_price_affordable_upgrade = max(affordable_upgrades)
            print(highest_price_affordable_upgrade)
            to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

            driver.find_element(By.ID, to_purchase_id).click()

            # Add another 5 seconds until the next check
            timeout = time.time() + 5

        # After 5 minutes stop the bot and check the cookies per second count.
        if time.time() > five_min:
            cookie_per_s = driver.find_element(By.ID, "cps").text
            print(cookie_per_s)
            break


def get_number_of_cookies():
    money_element = driver.find_element(By.ID, "money").text
    money_element = money_element.replace(",", "")
    return int(money_element)


def my_code(buy_time, stop_time):
    while True:
        cookie.click()
        if time.time() > buy_time:
            print("\nBuying most expense upgrade\n===================================")
            all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
            item_prices = []
            buy_time = time.time() + 5

            for price in all_prices:
                element_text = price.text
                if element_text != "":
                    cost = int(element_text.split("-")[1].strip().replace(",", ""))
                    item_prices.append(cost)

            # print(item_prices)

            cookie_upgrades = {}
            for n in range(len(item_prices)):
                cookie_upgrades[item_prices[n]] = item_ids[n]

            # print(cookie_upgrades)

            cookie_count = get_number_of_cookies()
            print(f"Available cookies:  {cookie_count}")

            affordable_upgrades = {}
            for cost, upgrade_id in cookie_upgrades.items():
                if cookie_count > cost:
                    affordable_upgrades[cost] = upgrade_id

            print(f"Affordable Upgrades:  {affordable_upgrades}")

            # purchase most expensive affordable upgrade
            most_expensive_upgrade = max(affordable_upgrades)
            # print(f"Most expensive affordable upgrade: {max(affordable_upgrades)}")
            purchase_id = affordable_upgrades[most_expensive_upgrade]
            print(f"==> {purchase_id}")
            driver.find_element(By.ID, purchase_id).click()

        if time.time() > stop_time:
            cookies_per_s = driver.find_element(By.ID, "cps").text
            print(f"\nEND\nCookies per second: {cookies_per_s}")
            break

    # driver.quit()


# working_code(timeout=PAUSE_TIMER, five_min=END_TIMER)
my_code(buy_time=time.time() + 5, stop_time=time.time() + 30)
