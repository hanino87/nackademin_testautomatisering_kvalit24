import libs.utils
from models.api.user import UserAPI
import requests

# set up BaseURL value to baseurl 

BASE_URL = "http://127.0.0.1:8000"

def test_signup():
    # Given I am a new potential customer
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()
    user_api = UserAPI(BASE_URL)
    # When I signup in the app
    signup_api_response = user_api.signup(username,password)
    assert signup_api_response.status_code == 200
    print(f"User signed up successfully with status {signup_api_response.status_code}")
    
    

def test_login():
    
    # Given I am an authenticated user​
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()
    user_api = UserAPI(BASE_URL)
    
    # Signup first so login will work
    user_api.signup(username,password)

    # When I log in into the application​ 
    token = user_api.login(username,password)
    token = user_api.login(username, password)
    assert token, "Login failed, no token received"
    print(f"Logged in token: {token}")
      
    #And i can see my products 
    user_api.get_user_all_products()
    products = user_api.get_user_all_products() 
    product_names = [p.get("name") for p in products if isinstance(p, dict)]
    assert not "apple" in product_names, "Expected 'apple' not to be in the product list"
    # assert that product list both can be empty and with products in it 
    # Extract just the product names
    
    products = products.get("products", [])   
    # product_names = [p.get("name") for p in products if isinstance(p, dict)]
    if len(products) == 0:
       assert len(products) == 0, f"Expected no products, but got {products}"
       print("✅ Product list is empty as expected.")
    else:
        assert len(products) > 0, "Expected some products, but got none"
        print(f"✅ Product list is not empty, found: {products}")
   
    
    
    
    

