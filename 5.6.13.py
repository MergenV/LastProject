import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

summa = 0


with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/infiniti_scroll_3/')
    browser.fullscreen_window()
    for elem in range(1,2):
        lst = []
        div = browser.find_element(By.XPATH, f'//*[@id="scroll-container_{elem}"]/div')
        for x in range(10):
            lst.extend(browser.find_elements(By.TAG_NAME, 'span'))
            ActionChains(browser).move_to_element(div).scroll_by_amount(1, 500).perform()
            time.sleep(1)
        print(len(set(lst)))






