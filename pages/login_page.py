from .base_page import BasePage
from .locators import LoginPageLocators


class LoginPage(BasePage):
    def should_be_login_page(self):
        self.should_be_login_url()
        self.should_be_login_form()
        self.should_be_register_form()

    def should_be_login_url(self):
        assert 'login' in self.browser.current_url, "URL не верный"

    def should_be_login_form(self):
        element = len(self.browser.find_elements(*LoginPageLocators.LOGIN_FORM))
        assert element>0, "не найдена форма Войти"

    def should_be_register_form(self):
        element = len(self.browser.find_elements(*LoginPageLocators.REGISTER_FORM))
        assert element>0, "не найдена форма Регистрация"

if __name__ == "__main__":
    pass
