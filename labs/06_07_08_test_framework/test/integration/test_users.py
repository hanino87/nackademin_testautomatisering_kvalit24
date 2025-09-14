import libs.utils
from models.api.user import UserAPI
import os 
from dotenv import load_dotenv

# Load .env once at the top of the test file
load_dotenv(dotenv_path="libs/.env")


def test_signup_and_login():
    """Sign up a new user and verify login works"""
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()
    base_url = os.getenv("BASE_URL_BACKEND")
    print("Backend URL:", os.getenv("BASE_URL_BACKEND"))
    user_api = UserAPI(base_url)

    # Signup
    signup_response = user_api.signup(username, password)
    assert signup_response.status_code == 200, f"Signup failed: {signup_response.text}"
    print(f"✅ User signed up successfully: {username}")

    # Login
    token = user_api.login(username, password)
    assert token, "Login failed, no token received"
    print(f"✅ Logged in successfully with token: {token}")


def test_user_product_list():
    """Login and verify the product list for a user"""
    base_url = os.getenv("BASE_URL_BACKEND")
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()
    user_api = UserAPI(base_url)

    # Ensure user exists
    user_api.signup(username, password)

    # Login
    token = user_api.login(username, password)
    assert token, "Login failed, no token received"

    # Get user's products
    products_response = user_api.get_user_all_products()
    products = products_response.get("products", []) if isinstance(products_response, dict) else []

    # Ensure products is a list
    assert isinstance(products, list), f"Expected list, got {type(products)}"

    # Extract product names
    product_names = [p.get("name") for p in products if isinstance(p, dict)]

    # Assert 'apple' is not in the list (admin removed previously)
    assert "apple" not in product_names, "Expected 'apple' not in product list"

    # Informative prints
    if not product_names:
        print("✅ Product list is empty as expected")
    else:
        print(f"✅ Product list contains: {product_names}")
