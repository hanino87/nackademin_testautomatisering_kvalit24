from test.test_config import login_as_admin

# -------------------------------------------------------
# Admin Integration tests (API) 
# -------------------------------------------------------
def test_add_product_to_catalog():
    admin_api = login_as_admin()
    new_products = ["apple", "banana"]
    for product in new_products:
        admin_api.create_product(product)
    after_names = [p.get("name") for p in admin_api.get_products_list()]
    for product in new_products:
        assert product in after_names

def test_remove_product_from_catalog():
    admin_api = login_as_admin()
    products_to_remove = ["apple", "banana"]
    for product in products_to_remove:
        admin_api.delete_product_by_name(product)
    after_names = [p.get("name") for p in admin_api.get_products_list()]
    for product in products_to_remove:
        assert product not in after_names
