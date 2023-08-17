
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
summa = 0
with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/scroll/3/')
    tags_input = browser.find_elements(By.TAG_NAME, 'input')

    for input in tags_input:
        input.send_keys(Keys.DOWN)
        input.click()
    for key, el in enumerate(browser.find_elements(By.TAG_NAME, 'span')):
        val = el.text
        if val:
            summa += int(tags_input[key].get_attribute('id'))
    print(summa)








