from .base_page import BasePage, check_wrapper
from .locators import ProductPageLocators
from selenium.webdriver.common.by import By

class ProductPage(BasePage):
	def __init__(self, *args, 
			name,
			full_name,
			price,
			promo=None):
		super().__init__(*args)
		self.name = name
		self.full_name = full_name
		self.price = price
		self.url += '/' + name
		if promo is not None:
			self.url += f'/?promo={promo}'

	def can_add_to_basket(self):
		try:
			add_button = self.driver.find_element(*ProductPageLocators.ADD_TO_BASKET)
			return add_button.is_enambled()
		except:
			return False

	def add_to_basket(self):
		try:
			add_button = self.driver.find_element(*ProductPageLocators.ADD_TO_BASKET)
			add_button.click()
		except Exception as e:
			print(e)

	@check_wrapper
	def should_be_success_message(self):
		full_name = self.driver.find_element(*ProductPageLocators.ALERT_PRODUCT_NAME).text
		assert self.full_name == full_name, 'Product was never added to basket'

	@check_wrapper
	def should_be_correct_price(self):
		price = self.driver.find_element(*ProductPageLocators.ALERT_INFO_PRICE).text[1:]
		assert self.price == float(price), 'Product price does not match total price'

	def should_be_added_to_basket(self):
		self.should_be_success_message()
		self.should_be_correct_price()

	def should_not_be_success_message(self, timeout=4):
		assert self.is_not_element_present(*ProductPageLocators.ALERT_PRODUCT_NAME, timeout),\
			'Success alert was never displayed'

	def should_not_desappear_success_message(self, timeout=4):
		assert not self.is_disappaered(*ProductPageLocators.ALERT_PRODUCT_NAME, timeout), \
			'Success alert was displayed but disappeared'






