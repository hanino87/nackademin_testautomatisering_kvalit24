from models.api.admin import AdminAPI
from models.api.user import UserAPI

def login_as_admin():
    """ helper function login as admin"""
    username = "admin"
    password = "admin1234"
    user_api = UserAPI("http://127.0.0.1:8000")
    token = user_api.login(username, password)
    assert token, "Admin login failed, no token returned"
    return AdminAPI("http://127.0.0.1:8000", token=token)


def test_add_product_to_catalog():
    """ validate admin can create a product to shop"""
    admin_api = login_as_admin()

    # Get initial products
    initial_products = admin_api.get_products_list()
    initial_names = [p.get("name") for p in initial_products]
    initial_count = len(initial_names)

    # Products to add
    new_products = ["apple", "banana"]

    # Add products only if they don't exist
    for product in new_products:
        if product not in initial_names:
            admin_api.create_product(product)

    # Get updated products
    products_after = admin_api.get_products_list()
    after_names = [p.get("name") for p in products_after]

    # Assertions
    for product in new_products:
        assert product in after_names, f"{product} not found in catalog after creation"

    # Count assertion: only count truly new products
    newly_added_count = sum(1 for p in new_products if p not in initial_names)
    new_count = admin_api.get_current_product_count()
    assert new_count == initial_count + newly_added_count, f"Expected {initial_count + newly_added_count}, got {new_count}"

    print("✅ Products after creation:", after_names)


def test_remove_product_from_catalog():
    """validate that admin can take away product from shop """
    admin_api = login_as_admin()

    # Products to remove
    products_to_remove = ["apple", "banana"]

    # Get initial products
    initial_products = admin_api.get_products_list()
    initial_names = [p.get("name") for p in initial_products]
    initial_count = len(initial_names)

    # Delete products only if they exist
    for product in products_to_remove:
        if product in initial_names:
            admin_api.delete_product_by_name(product)

    # Get updated products
    products_after = admin_api.get_products_list()
    after_names = [p.get("name") for p in products_after]

    # Assertions: removed products should not exist
    for product in products_to_remove:
        assert product not in after_names, f"{product} still found in catalog after deletion"

    # Count assertion: only decrease for products that actually existed
    deleted_count = sum(1 for p in products_to_remove if p in initial_names)
    new_count = admin_api.get_current_product_count()
    assert new_count == initial_count - deleted_count, f"Expected {initial_count - deleted_count}, got {new_count}"

    print("✅ Products after deletion:", after_names)
