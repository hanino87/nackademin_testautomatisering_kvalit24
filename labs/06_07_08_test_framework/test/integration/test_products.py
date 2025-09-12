from models.api.admin import AdminAPI
from models.api.user import UserAPI


"""Given I am an admin user​
   When I add a product to the catalog​
   Then The product is available to be used in the app"""

def test_add_product_to_catalog():
    # Given I am an admin user
    username = "admin"
    password = "admin1234"
    user_api = UserAPI("http://127.0.0.1:8000")
    # Login as admin and make sure it worked
    token = user_api.login(username, password)
    assert token, "Login failed, no token received"
    print(f"DEBUG: Logged in as admin, token = {token}")

    # Create AdminAPI with the valid token
    admin_api = AdminAPI(
        "http://127.0.0.1:8000",
        token=user_api.token   # same as token above
    )
    # Passing the token to the admin api # beacuse argument in the class is baseurl + token 

    admin_api.create_product("apple")
    
    # assert create_response.status_code == 200
    # Check that "apple" exists in catalog
    products = admin_api.get_products_list() # list of dicts
    # assert any(p.get("name") == "apple" for p in products)
    # Optionally check count
    count = admin_api.get_current_product_count()
    print(f"Current product count: {count}")
    assert count > 0,"Expected at least 1 product in catalog"
    print("Products in catalog:", products)

"""Given I am an admin user​
   When I remove a product from the catalog​
   Then The product should not be listed in the app to be used"""

def test_remove_product_from_catalog():
    username = "admin"
    password = "admin1234"

    # Create UserAPI instance
    user_api = UserAPI("http://localhost:8000")

    # Login first to get the token
    token = user_api.login(username, password)
    # asert that i have token for this response
    assert token, "Admin login failed, no token returned"
    print(f"DEBUG: Admin token = {token}")
    
    # Create AdminAPI instance with valid token
    admin_api = AdminAPI(
        "http://localhost:8000",
        token=token
    )
    # Now admin_api can perform admin actions safely
    
    # Delete the product
    admin_api.delete_product_by_name("apple")

    # Verify
    products = admin_api.get_products_list()
    print("DEBUG: products after creation:", products)# dict with "products" key
    products_after = admin_api.get_products_list()
    remaining_names = [p.get("name") for p in products_after]
    assert "apple" not in remaining_names
    print(f"✅ Products after deletion: {remaining_names}")
    
    
    
