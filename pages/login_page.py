from .base_page import BasePage, logger
from .locators import LoginPageLocators


class LoginPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_login = None
        self.current_password = None

    @logger
    def login_user(self, email, password, tries_left=2):
        try:
            self.driver.find_element(*LoginPageLocators.LOGIN_USERNAME_FIELD)\
                .send_keys(email)
            self.driver.find_element(*LoginPageLocators.LOGIN_PASSWORD_FIELD)\
                .send_keys(password)
            self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON)\
                .click()

            # Workaround for unexpected server errors.
            if 'server error' in self.driver.title.lower():
                if tries_left:
                    print(f'Server error occured, retrying, tries left: {tries_left}')
                    self.login_user(email, password, tries_left-1)
                else:
                    print('Failed to login user due to server error')
                    return
            else:
                print('Logged in user\n' + f'login: {email}, password: {password}')
                self._update_current_user_data(email, password)
        except:
            pass

    @logger
    def register_new_user(self, email, password):
        try:
            self.is_element_present(*LoginPageLocators.REGISTER_USERNAME_FIELD)
            self.driver.find_element(*LoginPageLocators.REGISTER_USERNAME_FIELD)\
                .send_keys(email)
            self.driver.find_element(*LoginPageLocators.REGISTER_PASSWORD_FIELD1)\
                .send_keys(password)
            self.driver.find_element(*LoginPageLocators.REGISTER_PASSWORD_FIELD2)\
            .send_keys(password)
            self.driver.find_element(*LoginPageLocators.REGISTER_BUTTON)\
                .click()
            print('Registered new user\n' + f'login: {email}, password: {password}')
        except:
            pass
        else:
            self._update_current_user_data(email, password)

    @logger
    def delete_user(self):
        '''
        Delete current active user. If no user is authorized, do nothing.
        '''

        if not self.should_be_authorized_user():
            return

        try:
            # Open account page.
            self.is_element_present(*LoginPageLocators.USER_ICON)
            self.driver.find_element(*LoginPageLocators.USER_ICON).click()
            # Press delete button.
            self.is_element_present(*LoginPageLocators.DELETE_USER_BUTTON)
            self.driver.find_element(*LoginPageLocators.DELETE_USER_BUTTON).click()
            # Confirm password and delete user.
            self.is_element_present(*LoginPageLocators.CONFIRMATION_FIELD)
            self.driver.find_element(*LoginPageLocators.CONFIRMATION_FIELD)\
                .send_keys(self.current_password)
            self.driver.find_element(*LoginPageLocators.CONFIRMATION_BUTTON).click()
        except:
            pass
        else:
            self._update_current_user_data(None, None)


    def should_be_login_page(self):
        self.should_be_login_url()
        self.should_be_login_form()
        self.should_be_register_form()

    def should_be_login_url(self):
        assert 'login' in self.driver.current_url, 'Incorrect URL'

    def should_be_login_form(self):
        assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), 'Login form not present'

    def should_be_register_form(self):
        assert self.is_element_present(*LoginPageLocators.REGISTER_FORM), 'Register form not present'

    def _update_current_user_data(self, email, password):
        self.current_login = email
        self.current_password = password