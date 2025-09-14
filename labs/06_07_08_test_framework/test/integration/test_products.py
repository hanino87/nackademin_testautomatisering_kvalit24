from models.api.admin import AdminAPI
from models.api.user import UserAPI


def test_add_product_to_catalog():
    # Given I am an admin user​
    username = "admin"
    password = "admin1234"
    user_api = UserAPI("http://127.0.0.1:8000")
    token = user_api.login(username, password)
    assert token, "Login failed, no token received"
    admin_api = AdminAPI("http://127.0.0.1:8000", token=token)
    initial_products = admin_api.get_products_list()
    initial_names = [p.get("name") for p in initial_products]
    initial_count = len(initial_names)

    # When I add a product to the catalog​
    admin_api.create_product("apple")
    admin_api.create_product("banana")
    products_after = admin_api.get_products_list()
    after_names = [p.get("name") for p in products_after]
    # Then The product is available to be used in the app"
    assert "apple" in after_names
    assert "banana" in after_names
    new_count = admin_api.get_current_product_count()
    assert new_count == initial_count + \
        2, f"Expected {initial_count + 2}, got {new_count}"

    print("✅ Products after creation:", products_after)


def test_remove_product_from_catalog():
    # Given I am an admin user​
    username = "admin"
    password = "admin1234"
    user_api = UserAPI("http://127.0.0.1:8000")
    token = user_api.login(username, password)
    assert token, "Admin login failed, no token returned"
    admin_api = AdminAPI("http://127.0.0.1:8000", token=token)

    # Get initial state
    products_before = admin_api.get_products_list()
    initial_count = len(products_before)
    exists = any(p.get("name") == "apple" for p in products_before)
    # When i delete the produt from the store
    admin_api.delete_product_by_name("apple")
    admin_api.delete_product_by_name("banana")

    # Then The product is not available to be used in the app"
    products_after = admin_api.get_products_list()
    remaining_names = [p.get("name") for p in products_after]
    assert "apple" not in remaining_names
    assert "banan" not in remaining_names

    # Verify count
    new_count = admin_api.get_current_product_count()
    if exists:
        assert new_count == initial_count - \
            2, f"Expected {initial_count - 2}, got {new_count}"
    else:
        assert new_count == initial_count, f"Expected {initial_count}, got {new_count}"

    print("✅ Products after deletion:", remaining_names)
