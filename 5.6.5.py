import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from itertools import product
options = Options()
options.add_argument("headless")

window_size_x = [616, 648, 680, 701, 730, 750, 805, 820, 855, 890, 955, 1000]
window_size_y = [300, 330, 340, 388, 400, 421, 474, 505, 557, 600, 653, 1000]
with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/window_size/2/index.html')
    for x, y in product(window_size_x, window_size_y):
        browser.set_window_size(x+42, y+170)
        time.sleep(3)
        value = browser.find_element(By.ID, 'result').text
        print(value)
        if value:
            print(value)
