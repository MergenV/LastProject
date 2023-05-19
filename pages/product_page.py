from .base_page import BasePage
from .locators import MainPageLocators, BasketPageLocators

class MainPage(BasePage):
    def go_to_basket_page(self):
        login_link = self.browser.find_element(*MainPageLocators.LOGIN_LINK)
        login_link.click()


    def should_be_login_link(self):
        assert self.is_element_present(*MainPageLocators.LOGIN_LINK), "Login link is not presented"

class BasketPage(BasePage):
    def check_item_in_cart(self):
        self.book_name_in_basket = self.browser.find_element(*BasketPageLocators.BOOK_NAME_IN_BASKET)
        self.book_name = self.browser.find_element(*BasketPageLocators.BOOK_NAME)
        self.book_price_in_basket = self.browser.find_element(*BasketPageLocators.BOOK_PRICE_IN_BASKET)
        self.book_price = self.browser.find_element(*BasketPageLocators.BOOK_PRICE)
        assert self.book_name.text == self.book_name_in_basket.text
        assert self.book_price.text == self.book_price_in_basket.text

