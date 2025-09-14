from playwright.sync_api import Page, expect
from models.ui.home import HomePage
from models.ui.admin import AdminPage
from models.api.user import UserAPI
import libs.utils


def test_add_product_to_catalog(page: Page):
    # Given I am an admin user​
    """login as admin user that is in the datbase before """
    username = "admin"
    password = "admin1234"
    home_page = HomePage(page)
    admin_page = AdminPage(page)
    user_api = UserAPI("http://localhost:8000")
    token = user_api.login(username, password)
    # Setting token through local storage to avoid logging in through the UI every time
    page.add_init_script(
        f"""
    window.localStorage.setItem("token", "{token}");
    """
    )
    home_page.navigate()
    before_count = len(admin_page.get_current_product_count())
    # When I add a product to the catalog​
    admin_page.create_product("fish")
    # Then The product is available to be used in the app
    # Wait for 'fish' specifically
    fish_locator = admin_page.page.locator(
        ".product-grid > .product-item > span", has_text="fish")
    expect(fish_locator).to_be_visible()

    after_products = admin_page.get_current_product_count()
    after_count = len(after_products)
    assert after_count == before_count + \
        1, f"Expected product count to increase by 1, but went from {before_count} to {after_count}"


def test_remove_product_from_catalog(page: Page):
    # Given I am an admin user​
    """ login as admin user that is in the datbase before """
    username = "admin"
    password = "admin1234"
    home_page = HomePage(page)
    admin_page = AdminPage(page)
    user_api = UserAPI("http://localhost:8000")
    token = user_api.login(username, password)
    # Setting token through local storage to avoid logging in through the UI every time
    page.add_init_script(
        f"""
    window.localStorage.setItem("token", "{token}");
    """
    )
    home_page.navigate()
    before_count = len(admin_page.get_current_product_count())
    # When I remove a product from the catalog​
    admin_page.delete_product_by_name("fish")
    # Wait until 'fish' is gone
    # Then The product should not be listed in the app to be used
    fish_locator = admin_page.page.locator(
        ".product-grid > .product-item > span", has_text="fish")
    expect(fish_locator).to_have_count(0)

    after_products = admin_page.get_current_product_count()
    after_count = len(after_products)
    assert after_count == before_count - \
        1, f"Expected product count to decrease by 1, but went from {before_count} to {after_count}"
