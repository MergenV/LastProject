from selenium.webdriver.common.by import By

class MainPageLocators():
    LOGIN_LINK = (By.CSS_SELECTOR, "button.btn-add-to-basket")

class LoginPageLocators():
    REGISTER_FORM = (By.CSS_SELECTOR, "form#register_form")
    LOGIN_FORM = (By.CSS_SELECTOR, "form#login_form")