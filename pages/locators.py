from selenium.webdriver.common.by import By

class BasePageLocators:
	URL = 'http://selenium1py.pythonanywhere.com/'
	LOGIN_LINK = (By.CSS_SELECTOR, '#login_link')
	USER_ICON = (By.CSS_SELECTOR, 'i.icon-user')

	BASKET_BUTTON = (By.CSS_SELECTOR, 'div.basket-mini a.btn')

class MainPageLocators(BasePageLocators):
	pass

class LoginPageLocators(BasePageLocators):
	URL = 'http://selenium1py.pythonanywhere.com/accounts/login/'
	LOGIN_FORM = (By.CSS_SELECTOR, '#login_form')
	REGISTER_FORM = (By.CSS_SELECTOR, '#register_form')

	LOGIN_USERNAME_FIELD = (By.CSS_SELECTOR, '#id_login-username')
	LOGIN_PASSWORD_FIELD = (By.CSS_SELECTOR, '#id_login-password')
	LOGIN_BUTTON = (By.XPATH, '//form[@id="login_form"] // button[contains(@class,"btn-lg")]')

	REGISTER_USERNAME_FIELD = (By.CSS_SELECTOR, '#id_registration-email')
	REGISTER_PASSWORD_FIELD1 = (By.CSS_SELECTOR, '#id_registration-password1')
	REGISTER_PASSWORD_FIELD2 = (By.CSS_SELECTOR, '#id_registration-password2')
	REGISTER_BUTTON = (By.XPATH, '//form[@id="register_form"] // button[contains(@class,"btn-lg")]')

	DELETE_USER_BUTTON = (By.CSS_SELECTOR, '#delete_profile')
	CONFIRMATION_FIELD = (By.CSS_SELECTOR, '#id_password')
	CONFIRMATION_BUTTON = (By.CSS_SELECTOR, 'button.btn-danger')

class BasketPageLocators(BasePageLocators):
	URL = 'http://selenium1py.pythonanywhere.com/basket/'
	BASKET_CONTENT = (By.CSS_SELECTOR, '#content_inner .basket-items')
	EMPTY_MESSAGE = (By.CSS_SELECTOR, '#content_inner p a')

class ProductPageLocators(BasePageLocators):
	URL = 'http://selenium1py.pythonanywhere.com/catalogue/'
	ADD_TO_BASKET = (By.CSS_SELECTOR, 'button.btn-add-to-basket')
	ALERT_PRODUCT_NAME = (By.CSS_SELECTOR, '.alert-success > .alertinner > strong')
	ALERT_INFO_PRICE = (By.CSS_SELECTOR, '.alert-info > div > p > strong')

'abcd@gmail.com'
'apassword'