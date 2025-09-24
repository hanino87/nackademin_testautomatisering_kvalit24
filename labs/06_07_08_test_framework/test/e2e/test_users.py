from playwright.sync_api import expect
from models.ui.home import HomePage
from models.ui.signup import SignupPage
from models.ui.user import UserPage
import libs.utils
from test.test_config import login_as_user
from pytest_bdd import scenarios, given, when, then
import os

FEATURE_FILE = os.path.join(os.path.dirname(__file__), '../../features/authentication.feature')
scenarios(FEATURE_FILE)

# -------------------------------------------------------
# BDD steps for testcase singup and login user 
# -------------------------------------------------------
@given("a new user with a unique username and password")
def given_new_user(page):
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()
    page.username = username
    page.password = password
    print(f"Given a new user: {username}")

@when("the user signs up via the UI")
def when_signup(page):
    username = page.username
    password = page.password

    page.on("dialog", lambda d: (print(f"⚠️ Dialog: {d.message}"), d.accept()))

    home_page = HomePage(page)
    signup_page = SignupPage(page)

    home_page.navigate()
    home_page.go_to_signup()
    signup_page.signup(username, password)
    page.wait_for_load_state("networkidle")
    signup_page.go_to_home()
    print(f"User signed up via UI: {username}")

@when("the user logs in via the UI")
def when_login(page):
    username = page.username
    password = page.password
    home_page = HomePage(page)
    home_page.login(username, password)
    print(f"User logged in via UI: {username}")

@then("the user should see a personalized welcome message") 
def then_see_welcome_message(page):
    username = page.username
    user_page = UserPage(page, username)
    home_page = HomePage(page)

    expect(user_page.welcome_message_with_username).to_be_visible()
    expect(user_page.welcome_message_with_username).to_contain_text(username)
    expect(home_page.login_input_username).to_be_hidden()
    expect(home_page.login_input_password).to_be_hidden()
    print(f"✅ Welcome message verified for user: {username}")


# -------------------------------------------------------
# User E2E tests (UI) 
# -------------------------------------------------------
def test_user_with_no_products(page):
    """Login and verify the product list is empty for a user without products"""
    user_page, _ = login_as_user(page, user_id=1)

    page.get_by_text("Loading user info").wait_for(state="hidden")
    no_products_locator = page.get_by_text("No products assigned.")
    no_products_locator.wait_for(state="visible")

    products = user_page.get_user_products()
    assert len(products) == 0
    assert no_products_locator.is_visible()
    print("✅ Products for USER1:", products)

def test_user_with_products(page):
    """Login and verify the product list has a laptop for a user with products"""
    user_page, _ = login_as_user(page, user_id=2)

    products = user_page.get_user_products()
    assert len(products) > 0
    assert any("laptop" == p.lower().strip() for p in products), "Laptop not found in product list."
    print("✅ Products for USER2:", products)
