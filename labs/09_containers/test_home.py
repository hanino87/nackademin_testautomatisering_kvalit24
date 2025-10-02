from playwright.sync_api import Page, expect
import os

APP_FRONT_URL=os.environ.get('APP_FRONT_URL')

def test_home_load(page: Page):
    page.goto(APP_FRONT_URL)
    page_header=page.get_by_text('Nackademin Course App')
    expect (page_header).to_be_visible()
    if page_header.is_visible():
        print("✅ 'Nackademin Course App' is visible on the page!")
    