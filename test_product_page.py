import time

from .pages.product_page import MainPage
from .pages.login_page import LoginPage
from selenium.webdriver.common.by import By
def test_guest_can_add_product_to_basket(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/?promo=newYear"
    page = MainPage(browser, link)
    page.open()
    page.go_to_basket_page()
    page.solve_quiz_and_get_code()


