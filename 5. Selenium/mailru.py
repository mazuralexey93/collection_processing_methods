"""
Вариант I
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
"""
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

my_login = input('логин: ')
pwd = input('пароль: ')
s = Service('./chromedriver.exe')

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=s,  options=options)

driver.get('https://account.mail.ru/login?')


login = driver.find_element(By.NAME, 'username')
login.send_keys(my_login)

pwd_button = driver.find_element(By.XPATH, "//button[@type='submit']")
pwd_button.click()
time.sleep(1)

pwd_input = driver.find_element(By.NAME, 'password')
pwd_input.send_keys(pwd)
pwd_input.send_keys(Keys.ENTER)
time.sleep(3)


def get_mails():
    # костылим счётчик, чтобы знать кол-во писем
    c_max = driver.find_element(By.XPATH, "//a[contains(@class, 'js-shortcut nav__item_active')] ").get_attribute('title').split(' ')[1]
    # c_max = 5
    c_cur = 0
    all_letters = []

    # заходим на 1 письмо
    link = driver.find_element(By.XPATH, "//a[contains(@class, 'llc')]").get_attribute('href')
    driver.get(link)

    # собираем информацию по письму, переходим к следующему
    while int(c_max) > c_cur:
        try:
            letter = {}
            sender = driver.find_element(By.CLASS_NAME, "letter-contact").text
            date = driver.find_element(By.CLASS_NAME, "letter__date").text
            theme = driver.find_element(By.CLASS_NAME, "thread-subject").text
            text = driver.find_element(By.CLASS_NAME, "letter-body").text

            letter['sender'] = sender
            letter['date'] = date
            letter['theme'] = theme
            letter['text'] = text

            all_letters.append(letter)

            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys(Keys.ARROW_DOWN).perform()
            c_cur += 1
            time.sleep(0.5)
        except:
            break

    print(len(all_letters))


get_mails()
