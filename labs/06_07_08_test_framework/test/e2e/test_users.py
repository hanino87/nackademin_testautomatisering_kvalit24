import pytest
from playwright.sync_api import Page, expect
from models.ui.home import HomePage
from models.ui.signup import SignupPage
from models.ui.user import UserPage
from models.api.user import UserAPI
import libs.utils


@pytest.fixture(scope="function")
def page_context(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def login_user(page_context: Page):
    """Return a function that logs in a user via API token."""
    def _login(username: str, password: str) -> UserPage:
        home_page = HomePage(page_context)
        user_page = UserPage(page_context, username)
        user_api = UserAPI("http://localhost:8000")
        token = user_api.login(username, password)
        page_context.add_init_script(f'window.localStorage.setItem("token", "{token}");')
        home_page.navigate()
        return user_page, home_page
    return _login



def test_signup(page_context: Page):
    """ validate login works for a new user to the store"""
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()

    home_page = HomePage(page_context)
    home_page.navigate()
    home_page.go_to_signup()

    signup_page = SignupPage(page_context)
    signup_page.signup(username, password)
    signup_page.go_to_home()

    home_page.login(username, password)
    user_page = UserPage(page_context, username)

    # Assertions
    expect(home_page.login_input_username).to_be_hidden()
    expect(home_page.login_input_password).to_be_hidden()
    expect(user_page.welcome_message_with_username).to_be_visible()
    expect(user_page.welcome_message_with_username).to_contain_text(username)
    print (user_page.welcome_message_with_username)

    user_page.logout()


def test_user_no_products(page_context: Page, login_user):
    """validate that user can log in and see it has no products """
    username = "userwithnoproduct"
    password = "user1234"

    user_page, _ = login_user(username, password)
    products = user_page.get_user_products()

    assert len(products) == 0
    no_products_locator = page_context.get_by_text("No products assigned.")
    assert no_products_locator.is_visible()
    print("✅ Products for the user it has no one as you can see:", products)


def test_user_with_products(page_context: Page, login_user):
    """validate that user can log in and see its products """
    username = "userwithproduct"
    password = "user1234"

    user_page, _ = login_user(username, password)
    products = user_page.get_user_products()

    assert len(products) > 0
    assert any("laptop" == p.lower().strip() for p in products), "Laptop not found in product list."
    print("✅ Products for the user:", products)
