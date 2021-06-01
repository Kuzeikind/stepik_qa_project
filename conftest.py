import pytest

from selenium import webdriver

def pytest_addoption(parser):
	'''
	Add --language command line option.
	'''
	lang_help_msg = 'Language ISO 639-1 code.\n'

	parser.addoption('--language',
                action='store',
                default='en-gb',
                help=lang_help_msg)

	headless_help_msg = 'Set the webdriver object used in test to be headless\n'

	parser.addoption('--headless',
	                action='store_true',
	                help=headless_help_msg)


@pytest.fixture(scope='function')
def driver(request):
	'''
	Set up a driver for tests with the options specified in the command line.
	'''
	# Configure driver options.
	opts = webdriver.ChromeOptions()

	language = request.config.getoption('language')
	opts.add_experimental_option('prefs', {'intl.accept_language': language})

	headless = request.config.getoption('headless')
	if headless:
		opts.add_argument('--headless')

	_driver = webdriver.Chrome(options=opts)
	
	yield _driver
	# Tear down
	_driver.close()
