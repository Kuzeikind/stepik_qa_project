from .pages.main_page import MainPage
from .pages.login_page import LoginPage
from .pages.basket_page import BasketPage
from .pages.product_page import ProductPage
from .pages.locators import *
from selenium import webdriver

import pytest

PRODUCTS = [
	{
	'name': 'the-shellcoders-handbook_209',
	'full_name': 'The shellcoder\'s handbook',
	'price': 9.99
	}
]

@pytest.mark.login_test
class TestLoginFromMainPage:
	def test_login_link_present(self, driver):
		main_page = MainPage(driver, MainPageLocators.URL)
		main_page.open()
		main_page.should_be_login_link()


	def test_user_can_go_to_login_page(self, driver):
		main_page = MainPage(driver, MainPageLocators.URL)
		main_page.open()
		main_page.go_to_login_page()

		login_page = LoginPage(driver, driver.current_url)
		login_page.should_be_login_page()


class TestBasket:
	def test_guest_cant_see_product_in_basket_opened_from_main_page(self, driver):
		basket_page = BasketPage(driver, BasketPageLocators.URL)
		basket_page.open()
		basket_page.should_be_empty()

	@pytest.mark.need_review
	@pytest.mark.parametrize('product', PRODUCTS)
	def test_guest_cant_see_product_in_basket_opened_from_product_page(self, driver, product):
		product_page = ProductPage(
			driver,
			ProductPageLocators.URL,
			**product)
		product_page.open()

		basket_page = BasketPage(driver, BasketPageLocators.URL)
		basket_page.open()
		basket_page.should_be_empty()
