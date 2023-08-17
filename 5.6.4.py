import time
from selenium.webdriver.common.by import By
from selenium import webdriver
summa = 0
with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/scroll/4/index.html')
    buttons = browser.find_elements(By.CLASS_NAME, 'btn')
    for item in buttons:
        browser.execute_script("return arguments[0].scrollIntoView(true);", item)
        item.click()
        summa += int(browser.find_element(By.ID, 'result').text)
    print(summa)






