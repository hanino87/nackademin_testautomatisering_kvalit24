from playwright.sync_api import sync_playwright, expect
from models.ui.home import HomePage
from models.ui.signup import SignupPage
from models.ui.user import UserPage
from models.api.user import UserAPI
import libs.utils
import os
from dotenv import load_dotenv
from pytest_bdd import scenarios, given, when, then

scenarios('../../features/my.feature')

load_dotenv(dotenv_path="libs/.env")

# """Feature: User Signup and Login authentication  

#   Scenario: New user can sign up and log in successfully
#     Given a new user with a unique username and password
#     When the user signs up via the UI
#     And the user logs in via the UI
#     Then the user should see a personalized welcome message""" 

@scenario('features/authentication.feature', 'New user can sign up and log in successfully')
def test_signup():
    pass 

@given("a new user with a unique username and password")
def given_new_user(page):
    print("Given a new user with a unique username and password")
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()
    # print(f"🧪 Username: {username}")
    # print(f"🧪 Password: {password}")
   
    # Store on page object for access in other steps
    page.username = username
    page.password = password
    
@when("the user signs up via the UI")
def when_signup(page):
    print("When the user signs up via the UI")
    # Store on page object for access in other steps
    username=page.username
    password=page.password

    # Handle all dialogs using a single lambda
    page.on("dialog", lambda d: (print(f"⚠️ Dialog: {d.message}"), d.accept()))

    # Page objects
    home_page = HomePage(page)
    signup_page = SignupPage(page)

    # When I signup in the app​
    home_page.navigate()
    home_page.go_to_signup()
    signup_page.signup(username, password)
    page.wait_for_load_state("networkidle") # do this for handle that backend is finished okay 
    signup_page.go_to_home()

@when("the user logs in via the UI")
def when_login(page):
    print("when the user logs in via the UI")
    
    username=page.username
    password=page.password
    home_page = HomePage(page)

    # Perform login via UI
    home_page.login(username, password)

@then("the user should see a personalized welcome message") 
def then_see_welcome_message(page):
    print("Then the user should see a personalized welcome message")
    home_page = HomePage(page)
    username=page.username
    
    # Then I should be able to log in with my new user
    user_page = UserPage(page, username)
    # user_page.welcome_message_with_username.wait_for(state="visible", timeout=10000)
    expect(user_page.welcome_message_with_username).to_be_visible()
    expect(user_page.welcome_message_with_username).to_contain_text(username)
    expect(home_page.login_input_username).to_be_hidden()
    expect(home_page.login_input_password).to_be_hidden()

def test_user_with_no_products(page):
    """validate that user can log in and see it has no products """
    username = os.getenv("USERNAME1")
    password = os.getenv("PASSWORD_USER1")
    user_page, _ = login_user(page, username, password)
    products = user_page.get_user_products()

    assert len(products) == 0
    no_products_locator = page.get_by_text("No products assigned.")
    assert no_products_locator.is_visible()
    print("✅ Products for the user it has no one as you can see:", products)


def test_user_with_products(page):
    """validate that user can log in and see its products """
    username = os.getenv("USERNAME2")
    password = os.getenv("PASSWORD_USER2")

    user_page, _ = login_user(page, username, password)
    products = user_page.get_user_products()

    assert len(products) > 0
    assert any("laptop" == p.lower().strip() for p in products), "Laptop not found in product list."
    print("✅ Products for the user:", products)
    
    
def login_user(page, username, password):
    """Login a user via API and inject token into localStorage."""
    home_page = HomePage(page)
    user_page = UserPage(page, username)
    user_api = UserAPI(os.getenv("BASE_URL_BACKEND"))
    token = user_api.login(username, password)
    page.add_init_script(f'window.localStorage.setItem("token", "{token}");')
    home_page.navigate()
    return user_page, home_page


"""User Products feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('features/user.feature', 'User with no products can see it has no products')
def test_user_with_no_products_can_see_it_has_no_products():
    """User with no products can see it has no products."""


@scenario('features/user.feature', 'User with products can see their products')
def test_user_with_products_can_see_their_products():
    """User with products can see their products."""


@given('a user with username "USERNAME1" and password "PASSWORD_USER1"')
def _():
    """a user with username "USERNAME1" and password "PASSWORD_USER1"."""
    raise NotImplementedError


@given('a user with username "USERNAME2" and password "PASSWORD_USER2"')
def _():
    """a user with username "USERNAME2" and password "PASSWORD_USER2"."""
    raise NotImplementedError


@when('the user logs in')
def _():
    """the user logs in."""
    raise NotImplementedError


@then('the product list should contain "Laptop"')
def _():
    """the product list should contain "Laptop"."""
    raise NotImplementedError


@then('the user should see no products')
def _():
    """the user should see no products."""
    raise NotImplementedError


@then('the user should see their products')
def _():
    """the user should see their products."""
    raise NotImplementedError