from .pages.login_page import LoginPage
from .pages.product_page import ProductPage
from .pages.locators import *
from selenium import webdriver

import pytest
import time


@pytest.fixture
def timer():
	start_time = time.time()
	yield
	time_taken = time.time() - start_time
	print('\n' + f'Time taken: {time_taken} seconds')

#==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ====
# The data for tests. Normally we would load it from the DB or some JSON files.
PRODUCTS = [
	{
	'name': 'the-shellcoders-handbook_209',
	'full_name': 'The shellcoder\'s handbook',
	'price': 9.99
	},
	{
	'name': 'coders-at-work_207',
	'full_name': 'Coders at Work',
	'price': 19.99
	},
	{
	'name': 'the-city-and-the-stars_95',
	'full_name': 'The City and the Stars',
	'price': 16.99
	}
]
PROMOS = ['offer'+str(i) for i in range(10)]
#==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ====

# Test adding products to basket.
class TestGuestAddProduct:
	@pytest.mark.need_review
	@pytest.mark.parametrize('promo', 
		[p if not p.endswith('7') else pytest.param('offer7', marks=pytest.mark.xfail) for p in PROMOS]
		) # a bit messy but truly automatized
	@pytest.mark.parametrize('product', PRODUCTS[1:2])
	def test_guest_can_add_product_to_basket(self, driver, product, promo):
		product_page = ProductPage(driver, 
			ProductPageLocators.URL,
			**product,
			promo=promo)
		product_page.open()
		product_page.add_to_basket()
		product_page.solve_quiz_and_get_code()
		product_page.should_be_added_to_basket()


# Test that the login page is available from any product page.
@pytest.mark.login_test
@pytest.mark.parametrize('product', PRODUCTS[2:3])
class TestLoginFromProductPage:
	def test_guest_can_see_login_link_on_product_page(self, driver, product):
		product_page = ProductPage(driver,
			ProductPageLocators.URL,
			**product)
		product_page.open()
		product_page.should_be_login_link()

	@pytest.mark.need_review
	def test_guest_can_go_to_login_page_from_product_page(self, driver, product):
		product_page = ProductPage(driver,
			ProductPageLocators.URL,
			**product)
		product_page.open()
		product_page.go_to_login_page()

		login_page = LoginPage(driver, driver.current_url)
		login_page.should_be_login_page()		


# Test that the success alert appears only when a new product is added.
@pytest.mark.usefixtures('timer')
@pytest.mark.parametrize('product', PRODUCTS[:1])
class TestGuestSuccessAlert:
	@pytest.mark.xfail
	def test_guest_cant_see_success_message_after_adding_product_to_basket(self, driver, product):
		product_page = ProductPage(driver, 
			ProductPageLocators.URL,
			**product)
		product_page.open()
		product_page.add_to_basket()
		product_page.should_not_be_success_message()

	def test_guest_cant_see_success_message(self, driver, product):
		product_page = ProductPage(driver, 
			ProductPageLocators.URL,
			**product)
		product_page.open()
		product_page.should_not_be_success_message()
	
	@pytest.mark.xfail				
	def test_message_disappeared_after_adding_product_to_basket(self, driver, product):
		product_page = ProductPage(driver, 
			ProductPageLocators.URL,
			**product)
		product_page.open()
		product_page.add_to_basket()
		product_page.should_not_desappear_success_message()


@pytest.fixture
def userdata():
	email = time.asctime().replace(' ', '_').replace(':', '-') + '@gmail.com'
	password = 'apassword'
	return (email, password)

@pytest.mark.login_test
@pytest.mark.parametrize('product', PRODUCTS[:1])
class TestUserAddProduct:
	@pytest.fixture(scope='function', autouse=True)
	def setup(self, driver, userdata):
		# Data
		email, password = userdata
		
		# Register.
		login_page = LoginPage(driver,
			LoginPageLocators.URL)
		login_page.open()
		login_page.register_new_user(email, password)

		# Verify that authorization was successful.
		login_page.should_be_authorized_user()

		yield

		# Delete newly registered user.
		login_page.delete_user()

	def test_user_cant_see_success_message(self, driver, product):
		product_page = ProductPage(driver, 
			ProductPageLocators.URL,
			**product)
		product_page.open()
		product_page.should_not_be_success_message()
	
	@pytest.mark.need_review
	def test_user_can_add_product_to_basket(self, driver, product):
		product_page = ProductPage(driver, 
			ProductPageLocators.URL,
			**product)
		product_page.open()
		product_page.add_to_basket()
		product_page.should_be_added_to_basket()

