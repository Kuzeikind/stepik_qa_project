import os

import pytest
from selenium import webdriver

_driver = None

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
	global _driver
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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
	pytest_html = item.config.pluginmanager.getplugin('html')
	outcome = yield
	report = outcome.get_result()
	extras = getattr(report, 'extra', [])

	# We only need screenshots while test are still running.
	if report.when in ('setup', 'call'):
		xfail = hasattr(report, 'wasxfail')
		if report.failed and not xfail:
			# Prepare the new screenshot path and respective web element.
			scrn_dir = _get_screen_dir()
			file_name = report.nodeid.replace('::', '_') + '.png'
			file_path = os.path.join(scrn_dir, file_name)
			html = f'<div><img src="file://{file_path}" alt="screenshot" '\
				'style="width:600px;height:228px:" onclick="window.open(this.src)"'\
				'align="right"/></div>'
			# Make a skreenshot and add it to extra.
			extras.append(pytest_html.extras.html(html))
			_capture_screen(file_path)
	report.extra = extras


def _get_screen_dir():
	# Potentially get the directory from a comman line option.
	cwd = os.path.dirname(__file__)
	scrn_dir = os.path.join(cwd, 'Screenshots')

	if not os.path.exists(scrn_dir):
		os.mkdir(scrn_dir)

	return scrn_dir


def _capture_screen(file_path):
	_driver.get_screenshot_as_file(file_path)