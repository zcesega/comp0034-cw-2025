from playwright.sync_api import Page, expect

def test_home_page_displayed(page: Page, app_server: str):
    page.goto(app_server)
    expect(page.locator("body")).to_be_visible()
    expect(page.get_by_role("link", name="Fleet Mix Shift Inspector")).to_be_visible()
