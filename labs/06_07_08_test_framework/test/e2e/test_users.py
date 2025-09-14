from playwright.sync_api import Page, expect
from models.ui.home import HomePage
from models.ui.signup import SignupPage
from models.ui.admin import AdminPage
from models.api.user import UserAPI
from models.ui.user import UserPage
import libs.utils
import pytest


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    return context.new_page()


def test_signup(page: Page):
    # Given I am a new potential customer​
    # Generates unique username and password for test
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()
    home_page = HomePage(page)
    home_page.navigate()
    home_page.go_to_signup()
    # When I signup in the app​
    sign_up = SignupPage(page)
    sign_up.signup(username, password)
    sign_up.go_to_home()
    home_page.login(username, password)
    user_page = UserPage(page, username)
    # Then I should be able to log in with my new user
    # confirms login by checking visible main title and that login elements are invisible
    expect(home_page.login_input_password).to_be_hidden()
    expect(home_page.login_input_username).to_be_hidden()
    expect(user_page.welcome_message_with_username).to_be_visible()
    # Is it the logged in user assert by se that username is part of the welcome message ?
    expect(user_page.welcome_message_with_username).to_contain_text(username)
    user_page.logout()


def test_login_and_see_products_for_user_that_has_no_products(page: Page):
    # Given I am an authenticated user​
    """User below has no produt beforde added in the database through postman/swagger """
    username = "userwithnoproduct"
    password = "user1234"
    home_page = HomePage(page)
    user_page = UserPage(page, username)
    user_api = UserAPI("http://localhost:8000")
    # When I log in into the application​
    token = user_api.login(username, password)
    # do this to skip login stage through frontend in test by passing token the localstorage direct on the page
    page.add_init_script(
        f"""
    window.localStorage.setItem("token", "{token}");
    """
    )
    home_page.navigate()
    # Then I should see all my products
    user_page.get_user_products()

    no_products_locator = page.get_by_text("No products assigned.")
    assert no_products_locator.is_visible()


def test_login_and_see_products_for_user_that_has_product(page: Page):
    # Given I am an authenticated user​
    """User below has product beforde added in the database through postman/swagger"""
    username = "userwithproduct"
    password = "user1234"
    home_page = HomePage(page)
    user_page = UserPage(page, username)
    user_api = UserAPI("http://localhost:8000")
    # When I log in into the application​
    token = user_api.login(username, password)
    # do this to skip login stage through frontend in test by passing token the localstorage direct on the page
    page.add_init_script(
        f"""
    window.localStorage.setItem("token", "{token}");
    """
    )
    home_page.navigate()
    # Then I should see all my products
    user_products = user_page.get_user_products()
    # this is independent that this tetuser has products before
    assert len(user_products) > 0
    # assert that any laptop is in the list even better for avoid case sensite issue like laptop with big L instead of small l
    assert any("laptop" == p.lower().strip()
               for p in user_products), "Laptop not found in product list."
