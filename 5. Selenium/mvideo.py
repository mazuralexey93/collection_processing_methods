"""
Вариант II
Написать программу, которая собирает товары «В тренде» с сайта
техники mvideo и складывает данные в БД. Главный критерий выбора: динамически загружаемые товары
"""
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


def mvidep_dynamic_content_parser():
    client = MongoClient('127.0.0.1', 27017)
    db = client['mvideo']
    trend = db.trend

    options = Options()
    options.add_argument("start-maximized")

    s = Service('./chromedriver')
    driver = webdriver.Chrome(service=s, options=options)

    driver.get("https://www.mvideo.ru")

    while True:
        try:
            button = driver.find_element(By.XPATH, "//button[@class='tab-button ng-star-inserted']")
            button.click()

            actions = ActionChains(driver)
            actions.send_keys(Keys.DOWN)
            actions.perform()
            time.sleep(1)
            break
        except:
            actions = ActionChains(driver)
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            time.sleep(1)

    carousel = driver.find_element(By.XPATH, "//mvid-carousel[contains(@class, 'carusel ng-star')]")
    items = carousel.find_elements(By.XPATH, "//mvid-carousel[contains(@class, 'carusel ng-star')]//div[@class = 'title']")
    price = driver.find_elements(By.XPATH, "//mvid-carousel[contains(@class, 'carusel ng-star')]\n"
                                             "//div[contains(@class, 'price')]//span[@class='price__main-value']")
    title = carousel.find_elements(By.XPATH, ".//div[contains(@class, '_name')]")
    link = carousel.find_elements(By.XPATH, ".//a")

    for i in range(len(items)):
        good = {
            'title': title[i].text,
            'link': link[i].get_attribute('href'),
            'price': price[i].text,
            '_id': str(link[i].get_attribute('href'))
        }

        try:
            trend.insert_one(good)
        except DuplicateKeyError:
            print(f' {good["_id"]} Already exists!')

    driver.close()


if __name__ == "__main__":
    mvidep_dynamic_content_parser()