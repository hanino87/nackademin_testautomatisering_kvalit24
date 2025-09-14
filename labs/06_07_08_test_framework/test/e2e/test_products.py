from playwright.sync_api import Page, expect
from models.ui.home import HomePage
from models.ui.admin import AdminPage
from models.api.user import UserAPI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="libs/.env")


def login_as_admin(page: Page):
    """Log in as admin via API token and return page objects. and load senstive stuff from env file"""
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    base_url = os.getenv("BASE_URL_BACKEND")
    

    home_page = HomePage(page)
    admin_page = AdminPage(page)
    user_api = UserAPI(base_url)

    token = user_api.login(username, password)
    # Set token directly in localStorage to skip UI login
    page.add_init_script(f'window.localStorage.setItem("token", "{token}");')
    home_page.navigate()
    return home_page, admin_page


def test_add_product_to_catalog(page: Page):
    """ validate admin can add product to shop """
    home_page, admin_page = login_as_admin(page)

    before_count = len(admin_page.get_current_product_count())
    admin_page.create_product("fish")

    # Wait specifically for 'fish'
    fish_locator = admin_page.page.locator(
        ".product-grid > .product-item > span", has_text="fish"
    )
    expect(fish_locator).to_be_visible()

    after_count = len(admin_page.get_current_product_count())
    assert after_count == before_count + 1, (
        f"Expected product count to increase by 1, but went from {before_count} to {after_count}"
    )
    existing_products=admin_page.get_current_product_count()
    print("✅ Products is in the store we now have 2 products:", existing_products)

def test_remove_product_from_catalog(page: Page,):
    """ validate admin can took away product from shop """
    home_page, admin_page = login_as_admin(page)

    before_count = len(admin_page.get_current_product_count())
    admin_page.delete_product_by_name("fish")

    # Wait until 'fish' is gone
    fish_locator = admin_page.page.locator(
        ".product-grid > .product-item > span", has_text="fish"
    )
    expect(fish_locator).to_have_count(0)

    after_count = len(admin_page.get_current_product_count())
    assert after_count == before_count - 1, (
        f"Expected product count to decrease by 1, but went from {before_count} to {after_count}"
    )
    existing_products=admin_page.get_current_product_count()
    print("✅ Products is out of the store we now only have 1 product:", existing_products)