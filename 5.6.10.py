import time
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
summa = 0
with webdriver.Chrome() as browser:
    browser.get('http://parsinger.ru/scroll/2/index.html')
    tags_input = browser.find_elements(By.TAG_NAME, 'input')

    for input in tags_input:
        input.send_keys(Keys.DOWN)
        input.click()
    for el in browser.find_elements(By.TAG_NAME, 'span'):
        val = el.text
        if val:
            summa += int(el.text)
    print(summa)






