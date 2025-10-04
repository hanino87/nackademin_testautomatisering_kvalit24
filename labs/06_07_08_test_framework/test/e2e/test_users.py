from playwright.sync_api import expect
from models.ui.home import HomePage
from models.ui.signup import SignupPage
from models.ui.user import UserPage
import libs.utils
from test.test_config import login_as_user

# -------------------------------------------------------
# User E2E tests (UI) 
# -------------------------------------------------------

def test_signup_and_login_user(page):
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()

    page.on("dialog", lambda d: d.accept())

    home = HomePage(page)
    signup = SignupPage(page)

    home.navigate()
    home.go_to_signup()
    signup.signup(username, password)
    page.wait_for_load_state("networkidle")
    signup.go_to_home()

    home.login(username, password)
    print(f"✅ User signed up via UI: {username} {password}")

    user = UserPage(page, username)

    expect(user.welcome_message_with_username).to_be_visible()
    expect(user.welcome_message_with_username).to_contain_text(username)
    expect(home.login_input_username).to_be_hidden()
    expect(home.login_input_password).to_be_hidden()

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
