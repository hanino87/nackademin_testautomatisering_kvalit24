from playwright.sync_api import expect
from models.ui.home import HomePage
from models.ui.signup import SignupPage
from models.ui.user import UserPage
import os
import requests
import libs.utils
from test.test_config import login_as_user

# -------------------------------------------------------
# User E2E tests (UI) 
# -------------------------------------------------------

def test_user_with_no_products(page):
    """Login and verify the product list is empty for a user without products"""
    user_page, _ = login_as_user(page, user_id=2)

    page.get_by_text("Loading user info").wait_for(state="hidden")
    no_products_locator = page.get_by_text("No products assigned.")
    no_products_locator.wait_for(state="visible")

    products = user_page.get_user_products()
    assert len(products) == 0
    assert no_products_locator.is_visible()
    print("✅ Products for USER1 as you can see it has no products:", products)




def test_signup_and_login_user(page):
    username = libs.utils.generate_string_with_prefix()
    password = libs.utils.generate_password_with_prefix()

    # Accept any JS dialogs
    #page.on("dialog", lambda d: d.accept())

    home = HomePage(page)
    signup = SignupPage(page)

    # Ensure screenshots folder exists
    screenshots_dir = "/var/jenkins_home/workspace/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    # 1️⃣ Navigate to signup and create user
    home.navigate()
    home.go_to_signup()
    with page.expect_event("dialog") as dialog_info:
     signup.signup(username, password)
    dialog = dialog_info.value
    dialog.accept()
    page.wait_for_load_state("networkidle")
    signup.go_to_home()
    page.wait_for_load_state("networkidle")
    print(f"✅ User signed up via UI: {username} {password}")

    # 2️⃣ Check backend is reachable
    try:
        response = requests.get("http://app-backend:8000/health", timeout=5)
        assert response.status_code == 200, "Backend health check failed!"
        print("✅ Backend reachable")
    except Exception as e:
        print("⚠️ Backend not reachable from Jenkins:", e)
        # Capture page for debugging
        page.screenshot(path=os.path.join(screenshots_dir, "login_state.png"))
        with open(os.path.join(screenshots_dir, "login_state.html"), "w") as f:
            f.write(page.content())
        raise e

    # 3️⃣ Perform login
    try:
        # Wait for login button to be enabled
        expect(home.login_btn_login).to_be_enabled(timeout=10000)

        home.login(username, password)
        page.wait_for_load_state("networkidle")
        print(f"✅ User logged in via UI: {username} {password}")

        # 4️⃣ Wait for welcome message to confirm login
        user = UserPage(page, username)
        user.welcome_message_with_username.wait_for(state="visible", timeout=15000)

        # 5️⃣ Assertions
        expect(user.welcome_message_with_username).to_be_visible()
        expect(user.welcome_message_with_username).to_contain_text(username)
        expect(home.login_input_username).to_be_hidden()
        expect(home.login_input_password).to_be_hidden()

    except Exception as e:
        # Capture page for debugging if login fails
        page.screenshot(path=os.path.join(screenshots_dir, "login_state.png"))
        with open(os.path.join(screenshots_dir, "login_state.html"), "w") as f:
            f.write(page.content())
        print("📸 Screenshot and HTML saved for debugging")
        raise e

    
# -------------------------------------------------------
# User E2E tests (UI) This test will be implemented when user can add products
# -------------------------------------------------------

 
def test_user_with_products(page):
    """Login and verify the product list has a laptop for a user with products"""
    user_page, _ = login_as_user(page, user_id=2,)
    user_page.add_product_to_user()
    laptop_locator = page.locator("#root div div div div", has_text="Laptop")
    expect(laptop_locator).to_be_visible()
    
    if laptop_locator.is_visible():
        print("✅ Laptop is visible in the product list")
    else:
          print("⚠️ Laptop is NOT visible in the product list we raise a bug to the developer")

    # Ta bort produkten
    user_page.remove_product_from_user()
    expect(laptop_locator).to_be_hidden()

    # Kolla igen efter borttagning
    if laptop_locator.is_visible():
      print("⚠️ Laptop is still visible after removal")
    else:
        print("✅ Laptop is now hidden after removal")
        
    

   