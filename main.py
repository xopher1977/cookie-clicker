#! Don't run this at work!
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
export_save = driver.find_element(By.ID, "exportSave")
import_save = driver.find_element(By.ID, "importSave")
reset = driver.find_element(By.ID, "reset")

# for upgrade in upgrades:
#     upgrade_ids.append(upgrade.get_attribute("id"))

# Get upgrade item ids.
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

PAUSE_TIMER = time.time() + 5
END_TIMER = time.time() + 60 * 15  # 15 minutes


def get_number_of_cookies():
    money_element = driver.find_element(By.ID, "money").text
    money_element = money_element.replace(",", "")
    return int(money_element)


def make_cookies(buy_time, stop_time):
    # pdb.set_trace()
    try:
        with open("data/save.data", "r") as input:
            code = input.readline()
    except FileNotFoundError:
        print("No saved data found")
        code = None

    if code:
        driver.execute_script("ImportResponse('1|" + code + "');")
    while True:
        cookie.click()
        if time.time() > buy_time:
            print("\nBuying most expensive upgrade\n===================================")
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

            if len(affordable_upgrades) > 0:
                # purchase most expensive affordable upgrade
                most_expensive_upgrade = max(affordable_upgrades)
                # print(f"Most expensive affordable upgrade: {max(affordable_upgrades)}")
                purchase_id = affordable_upgrades[most_expensive_upgrade]
                print(f"==> {purchase_id}")
                driver.find_element(By.ID, purchase_id).click()
            else:
                print("Sorry, you don't have enough cookies to purchase any upgrades at the moment.  Keep making "
                      "cookies!!!")

        if time.time() > stop_time:
            cookies_per_s = driver.find_element(By.ID, "cps").text
            print(f"\nEND\nCookies per second: {cookies_per_s}")
            # pdb.set_trace()
            save_string = driver.execute_script("return MakeSaveString();")
            with open("data/save.data", "w") as file:
                file.write(save_string)
            break

    time.sleep(5)
    driver.quit()


make_cookies(buy_time=PAUSE_TIMER, stop_time=END_TIMER)
