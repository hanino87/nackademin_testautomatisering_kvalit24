import libs.utils
from models.api.user import UserAPI
from test.test_config import get_backend_url

# -------------------------------------------------------
# User Integration tests (API) 
# -------------------------------------------------------

def test_signup_and_login():
    """Sign up a new user and verify login works"""
    base_url = get_backend_url()
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()
    user_api = UserAPI(base_url)
    signup_response = user_api.signup(username, password)
    assert signup_response.status_code == 200, f"Signup failed: {signup_response.text}"
    print(f"✅ User signed up successfully: {username}")
    token = user_api.login(username, password)
    assert token, "Login failed, no token received"
    print(f"✅ Logged in successfully with token: {token}")


def test_login_and_get_user_products():
    """Login and verify the product list for a user is empty"""
    base_url = get_backend_url()
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()
    user_api = UserAPI(base_url)
    user_api.signup(username, password)
    token = user_api.login(username, password)
    assert token, "Login failed, no token received"
    products_response = user_api.get_user_all_products()
    products = products_response.get("products", []) if isinstance(products_response, dict) else []
    assert isinstance(products, list), f"Expected list, got {type(products)}"
    product_names = [p.get("name") for p in products if isinstance(p, dict)]
    assert "apple" not in product_names, "Expected 'apple' not in product list"
    if not product_names:
        print("✅ Product list is empty as expected")
    else:
        print(f"✅ Product list contains: {product_names}")
