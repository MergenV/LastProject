import time
from selenium.webdriver.common.by import By
from selenium import webdriver
sites = ['http://parsinger.ru/blank/1/1.html', 'http://parsinger.ru/blank/1/2.html', 'http://parsinger.ru/blank/1/3.html',
         'http://parsinger.ru/blank/1/4.html', 'http://parsinger.ru/blank/1/5.html', 'http://parsinger.ru/blank/1/6.html',]
summa = 0
with webdriver.Chrome() as browser:
    for key, url in enumerate(sites):
        browser.execute_script(f'window.open("{url}", "_blank{key}");')
        time.sleep(1)
    for x in range(
            len(browser.window_handles)):  # reversed(range(len(browser.window_handles))) Для итерирования по порядку
        browser.switch_to.window(browser.window_handles[x])
        for y in browser.find_elements(By.CLASS_NAME, 'checkbox_class'):
            y.click()
            summa += int(browser.find_element(By.ID, 'result').text)**0.5
            time.sleep(1)
print(round(summa,9))






