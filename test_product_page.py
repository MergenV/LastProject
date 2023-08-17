import time

from .pages.product_page import MainPage, BasketPage, PoductPage
import pytest
LINK = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
list_of_failed_num = [7]
tested_links = [f"{LINK}?promo=offer{i}" if i not in list_of_failed_num else
                pytest.param(f"{LINK}?promo=offer{i}",
                             marks=pytest.mark.xfail(reason="some bug", strict=True)
                             )
                for i in range(10)]
@pytest.mark.parametrize("link", tested_links)
def test_guest_can_add_product_to_basket(browser, link):
    page = MainPage(browser, link)
    page.open()
    page.go_to_basket_page()
    page.solve_quiz_and_get_code()
    basket_page = BasketPage(browser,link)
    basket_page.check_item_in_cart()

def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    product_page = PoductPage(browser, link, 4)
    product_page.open()





