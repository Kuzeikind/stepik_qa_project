from .locators import BasePageLocators
from selenium.common.exceptions import (NoSuchElementException,
										NoAlertPresentException,
										TimeoutException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from functools import wraps
import logging


class BasePage:
	def __init__(self, driver, url, timeout=4):
		self.driver = driver
		self.url = url
		self.timeout = timeout

	def go_to_login_page(self):
		login_link = self.driver.find_element(*BasePageLocators.LOGIN_LINK)
		login_link.click()

	def is_disappeared(self, locator, selector, timeout=None):
		if timeout is None:
			timeout = self.timeout
		try:
			WebDriverWait(self.driver, timeout).\
				until_not(EC.presence_of_element_located((locator, selector)))
		except TimeoutException:
			return False
		return True

	def is_element_present(self, locator, selector, timeout=None):
		if timeout is None:
			timeout = self.timeout
		try:
			WebDriverWait(self.driver, timeout).\
				until(EC.presence_of_element_located((locator, selector)))
		except TimeoutException:
			return False
		return True

	def is_not_element_present(self, locator, selector, timeout=None):
		if timeout is None:
			timeout = self.timeout
		try:
			WebDriverWait(self.driver, timeout).\
				until(EC.presence_of_element_located((locator, selector)))
		except TimeoutException:
			return True
		return False

	def open(self):
		self.driver.get(self.url)

	def should_be_authorized_user(self):
		assert self.is_element_present(*BasePageLocators.USER_ICON),\
			'User icon not present, probably not authorized user'

	def should_be_login_link(self):
		assert self.is_element_present(*BasePageLocators.LOGIN_LINK), 'Login link not present'

	def solve_quiz_and_get_code(self):
		from math import log, sin

		alert = self.driver.switch_to.alert
		x = alert.text.split(" ")[2]
		answer = str(log(abs((12 * sin(float(x))))))
		alert.send_keys(answer)
		alert.accept()

		try:
			alert = self.driver.switch_to.alert
			alert_text = alert.text
			print(f"Your code: {alert_text}")
			alert.accept()
		except NoAlertPresentException:
			print("No second alert present")



def check_wrapper(func):
	'''
	Decorator for checking methods that only allows AssertionError and catches
	all other exceptions. This makes tests fail safely without crashing the 
	script.
	'''
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			func(*args, **kwargs)
		except AssertionError as ae:
			raise ae
		except Exception as e:
			print(e)
			assert False, 'Unexpected problem occured'
	return wrapper


def logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
    	# Check if the function is actually a class method.
        # Remove `self` from the args list for logging if so.
        is_method = 0
        if 'self' in func.__code__.co_varnames:
            is_method = 1

        # Log the info.
        logging.info(
            f'{func.__name__} called with {args[is_method:]}, {kwargs}'
            )
        # Run the function.
        result = func(*args, **kwargs)
        return result
    
    return wrapper
