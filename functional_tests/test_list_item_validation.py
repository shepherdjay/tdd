def test_cannot_add_empty_list_items(live_server, browser):
    # Edith goes to the home page and accidentally tries to submit
    # an empty list item. She hits Enter on the empty input box
    browser.get(live_server.url)
    browser.get_item_input_box().send_keys('\n')

    # The home page refreshes, and there is an error message saying
    # that list items cannot be blank
    error = browser.get_error_element()
    assert "You can't have an empty list item" == error.text

    # She tries again with some text for the item, which now works
    browser.get_item_input_box().send_keys('Buy milk\n')
    browser.check_for_row_in_list_table('1: Buy milk')

    # Perversely, she now decides to submit a second blank list item
    browser.get_item_input_box().send_keys('\n')

    # She receives a similar warning on the list page
    browser.check_for_row_in_list_table('1: Buy milk')
    error = browser.get_error_element()
    assert "You can't have an empty list item" == error.text

    # And she can correct it by filling some text in
    browser.get_item_input_box().send_keys('Make tea\n')
    browser.check_for_row_in_list_table('1: Buy milk')
    browser.check_for_row_in_list_table('2: Make tea')


def test_cannot_add_duplicate_items(live_server, browser):
    # Edith goes to the home page and starts a new list
    browser.get(live_server.url)
    browser.get_item_input_box().send_keys('Buy wellies\n')
    browser.check_for_row_in_list_table('1: Buy wellies')

    # She accidentally tries to enter a duplicate item
    browser.get_item_input_box().send_keys('Buy wellies\n')

    # She sees a helpful error message
    browser.check_for_row_in_list_table('1: Buy wellies')
    error = browser.get_error_element()
    assert "You've already got this in your list" == error.text


def test_error_messages_are_cleared_on_input(live_server, browser):
    # Edith starts a new list in a way that causes a validation error:
    browser.get(live_server.url)
    browser.get_item_input_box().send_keys('\n')
    error = browser.get_error_element()
    assert error.is_displayed()

    # She starts typing in the input box to clear the error
    browser.get_item_input_box().send_keys('a')

    # She is pleased to see that the error message disappears
    error = browser.get_error_element()
    assert not error.is_displayed()
