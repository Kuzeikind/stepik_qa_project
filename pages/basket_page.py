from .locators import BasketPageLocators
from .base_page import BasePage

class BasketPage(BasePage):
	def should_be_empty(self):
		assert self.is_element_present(*BasketPageLocators.EMPTY_MESSAGE),\
			'No empty message present'
		assert self.is_not_element_present(*BasketPageLocators.BASKET_CONTENT),\
			'Basket contains some products, is not empty'

	def should_not_be_empty(self):
		assert self.is_element_present(*BasketPageLocators.BASKET_CONTENT),\
			'No products found in basket'
