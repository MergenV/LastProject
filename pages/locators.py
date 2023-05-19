from selenium.webdriver.common.by import By

class MainPageLocators():
    LOGIN_LINK = (By.CSS_SELECTOR, "button.btn-add-to-basket")

class LoginPageLocators():
    REGISTER_FORM = (By.CSS_SELECTOR, "form#register_form")
    LOGIN_FORM = (By.CSS_SELECTOR, "form#login_form")

class BasketPageLocators():
    BOOK_NAME_IN_BASKET = (By.XPATH, "//div[@id='messages']/div[1]/div/strong")
    BOOK_NAME = (By.XPATH, "//h1")
    BOOK_PRICE_IN_BASKET = (By.XPATH, "//div/div/div/div/div/p/strong")
    BOOK_PRICE = (By.CSS_SELECTOR, "p.price_color")