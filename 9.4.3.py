import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha


def solver(question):
    solver = TwoCaptcha('16c0dd81669d47298b48a2b849698b67')
    print('Вопрос отправился на решение:', question)
    result = solver.text(question)
    print('От API пришёл ответ: ', result)
    return result['code']


with webdriver.Chrome() as browser:
    browser.get('https://captcha-parsinger.ru/text?page=3')
    browser.maximize_window()
    time.sleep(2)
    question_text = browser.find_element(By.CSS_SELECTOR, 'div[class="chakra-form-control css-1sx6owr"]').find_element(
        By.TAG_NAME, 'p').text
    tag_input = browser.find_element(By.ID, 'field-:r0:')
    tag_input.send_keys(solver(question_text))
    elem_button = browser.find_element(By.CSS_SELECTOR, 'button[class="chakra-button css-1wq39mj"]')
    elem_button.click()
    time.sleep(1)
    while True:
      #На первой итерации цикла cписок name_card=[] может быть пустым, если первое решение капчи было не
      #верное, тогда мы сразу переходит в ветку else

        name_card = [x.text for x in browser.find_elements(By.CLASS_NAME, 'css-5ev4sb')]
        if len(name_card) > 0:
            print('Решение верное, данные получены')
            print(name_card)
            break
        else:
            print('Решение не верное, ещё попытка')
            browser.find_element(By.ID, 'field-:r0:').send_keys(solver(question_text))
            elem_button.click()
            time.sleep(1)
            [name_card.append(x.text) for x in browser.find_elements(By.CLASS_NAME, 'css-5ev4sb')]
    articles = [int(el.text.split()[1]) for el in browser.find_elements(By.XPATH, "//div[@class='css-1ecvsm5']/ul/li[1]")]

print(sum(articles))