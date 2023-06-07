from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re


def test_can_start_a_list_and_retrieve_it_later(live_server, browser):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get(live_server.url)

    # She notices the page title and header mention to-do lists
    assert 'To-Do' in browser.title
    header_text = browser.find_element(By.TAG_NAME, 'h1').text
    assert 'To-Do' in header_text

    # She is invited to enter a to-do item straight away
    inputbox = browser.get_item_input_box()
    assert 'Enter a to-do item' == inputbox.get_attribute('placeholder')

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    inputbox.send_keys('Buy peacock feathers')

    # When she hits enter, she is taken to a new url,
    # and now the page lists "1: Buy peacock feathers"
    # as an item in a to-do list table
    inputbox.send_keys(Keys.ENTER)
    edith_list_url = browser.current_url
    assert re.search(r'/lists/.+', edith_list_url)
    browser.check_for_row_in_list_table("1: Buy peacock feathers")

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox = browser.get_item_input_box()
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on her list
    browser.check_for_row_in_list_table("1: Buy peacock feathers")
    browser.check_for_row_in_list_table("2: Use peacock feathers to make a fly")

    # Now a new user, Francis, comes along to the site.

    # Clear the browser of all cookies
    browser.clear_browser()

    # Francis visits the home page. There is no sign of Edith's
    # list
    browser.get(live_server.url)
    page_text = browser.find_element(By.TAG_NAME,'body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'make a fly' not in page_text

    # Francis starts a new list by entering a new item. He
    # is less interesting than Edith..
    inputbox = browser.get_item_input_box()
    inputbox.send_keys('Buy milk')
    inputbox.send_keys(Keys.ENTER)

    # Francis gets his own unique url
    francis_lists_url = browser.current_url
    assert re.search(r'/lists/.+', francis_lists_url)
    assert edith_list_url != francis_lists_url

    # Again, there is no trace of Edith's list
    page_text = browser.find_element(By.TAG_NAME, 'body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'Buy milk' in page_text

    # Satisfied they both go back to sleep
