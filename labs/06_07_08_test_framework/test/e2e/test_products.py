from playwright.sync_api import Page, expect
from models.ui.home import HomePage
from models.ui.admin import AdminPage
from models.api.user import UserAPI
from dotenv import load_dotenv
import os

# Load sensitive data from .env
load_dotenv(dotenv_path="libs/.env")

def login_as_admin(page: Page):
    """Log in as admin via API token and return page objects."""
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    base_url = os.getenv("BASE_URL_BACKEND")

    token = UserAPI(base_url).login(username, password)
    page.add_init_script(f'window.localStorage.setItem("token", "{token}");')

    home_page = HomePage(page)
    home_page.navigate()
    return home_page, AdminPage(page)


def test_add_product_to_catalog(page: Page):
    """Validate admin can add product to shop."""
    home_page, admin_page = login_as_admin(page)
    admin_page.create_product("fish")
    fish_locator = admin_page.page.locator(".product-grid span", has_text="fish")
    expect(fish_locator).to_be_visible()
    total_products = len(admin_page.get_current_product_count())
    assert total_products == 2, (
        f"Expected product basket to have 1 item count to increase by 2, but went it has not 2 items"
    )
    print("✅ Product added. Total products:", total_products)


def test_remove_product_from_catalog(page: Page):
    """Validate admin can remove product from shop."""
    home_page, admin_page = login_as_admin(page)
    admin_page.delete_product_by_name("fish")

    fish_locator = admin_page.page.locator(".product-grid span", has_text="fish")
    expect(fish_locator).to_be_hidden()
    
    total_products = len(admin_page.get_current_product_count())
    assert total_products == 1, (
        f"Expected product basket to have 1 item count to increase by 2, but it has not 2 items"
    )
    print("✅ Product added. Total products:", total_products)

    # assert that empty basket message is not visible on the page 
    empty_basket_message=admin_page.no_products_header_text
    expect(empty_basket_message).to_be_hidden()
    if empty_basket_message.is_hidden():
     print("✅ Product is gone. Total products: 1")
    else:
      print("❌ Ah i see the empty basket message we raise a bug to developet 1 products should be in the list")
   

