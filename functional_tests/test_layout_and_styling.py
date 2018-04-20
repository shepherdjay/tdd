import pytest


def test_layout_and_styling(live_server, browser):
    # Edith goes to the home page
    browser.get(live_server.url)
    browser.set_window_size(1024, 768)

    # She notices the input box is nicely centered
    inputbox = browser.get_item_input_box()
    assert inputbox.location['x'] + inputbox.size['width'] / 2 == pytest.approx(512, abs=10)

    # She starts a new list and sees the input is nicely
    # centered there too
    inputbox.send_keys('testing\n')
    inputbox = browser.get_item_input_box()
    assert inputbox.location['x'] + inputbox.size['width'] / 2 == pytest.approx(512, abs=10)
