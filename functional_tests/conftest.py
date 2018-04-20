import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Browser:
    def __init__(self, browser):
        self.browser = browser

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        assert row_text in [row.text for row in rows]

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def clear_browser(self):
        self.browser.delete_all_cookies()
        self.browser.refresh()


    # Pass any unknown calls to the underlying web driver object
    def __getattr__(self, attr):
        return getattr(self.browser, attr)


@pytest.fixture()
def chrome_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.implicitly_wait(10)
    yield browser
    browser.refresh()
    browser.quit()


@pytest.fixture()
def browser(chrome_browser):
    return Browser(chrome_browser)
