from playwright.sync_api import sync_playwright, expect
from models.ui.home import HomePage
from models.ui.signup import SignupPage
from models.ui.user import UserPage
from models.api.user import UserAPI
import libs.utils
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="libs/.env")

def login_user(page, username, password):
    """Login a user via API and inject token into localStorage."""
    home_page = HomePage(page)
    user_page = UserPage(page, username)
    user_api = UserAPI(os.getenv("BASE_URL_BACKEND"))
    token = user_api.login(username, password)
    page.add_init_script(f'window.localStorage.setItem("token", "{token}");')
    home_page.navigate()
    return user_page, home_page

def test_signup(page):
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()
    print(f"🧪 Username: {username}")
    print(f"🧪 Password: {password}")

    # Handle all dialogs using a single lambda
    page.on("dialog", lambda d: (print(f"⚠️ Dialog: {d.message}"), d.accept()))

    # Page objects
    home_page = HomePage(page)
    signup_page = SignupPage(page)

    # Navigate and perform signup
    home_page.navigate()
    home_page.go_to_signup()
    signup_page.signup(username, password)
    page.wait_for_load_state("networkidle") # do this for handle that backend is finished okay 
    signup_page.go_to_home()

    # Perform login via UI
    home_page.login(username, password)

    # Validate user login
    user_page = UserPage(page, username)
    # user_page.welcome_message_with_username.wait_for(state="visible", timeout=10000)
    expect(user_page.welcome_message_with_username).to_be_visible()
    expect(user_page.welcome_message_with_username).to_contain_text(username)
    expect(home_page.login_input_username).to_be_hidden()
    expect(home_page.login_input_password).to_be_hidden()

def test_user_no_products(page):
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
    
    
  