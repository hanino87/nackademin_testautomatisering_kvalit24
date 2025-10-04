# libs/config.py
import os
from dotenv import load_dotenv
from models.api.user import UserAPI
import requests

# Load .env once
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=dotenv_path)

# ----------------------------
# Prepare that Testdata User is before test 
# ----------------------------

def ensure_admin_exists():
    """Ensure the first user (admin) exists.
    If DB is empty, /signup will create the admin.
    If user already exists, backend should return 400/409 and we ignore it.
    """
    base_url = get_backend_url()
    username, password = get_admin_credentials()

    print(f"Ensuring admin exists via {base_url}/signup ...")

    resp = requests.post(
        f"{base_url}/signup",
        json={"username": username, "password": password}
    )

    if resp.status_code == 201:
        print("✅ Admin created successfully (first user in DB).")
    elif resp.status_code in (400, 409):
        print("ℹ️ Admin already exists, continuing...")
    else:
        print(f"⚠️ Unexpected response {resp.status_code}: {resp.text}")
        resp.raise_for_status()


def ensure_user_exists(user_id: int = 1):
    """Ensure a given user exists.
    If DB only has admin, /signup will create this user.
    If user already exists, backend should return 400/409 and we ignore it.
    """
    base_url = get_backend_url()
    username, password = get_user_credentials(user_id=user_id)

    print(f"Ensuring {username} (user_id={user_id}) exists via {base_url}/signup ...")

    resp = requests.post(
        f"{base_url}/signup",
        json={"username": username, "password": password}
    )

    if resp.status_code == 201:
        print(f"✅ {username} created successfully.")
    elif resp.status_code in (400, 409):
        print(f"ℹ️ {username} already exists, continuing...")
    else:
        print(f"⚠️ Unexpected response {resp.status_code}: {resp.text}")
        resp.raise_for_status()



def ensure_product_exists(page, product_name: str = "laptop"):
    """Ensure a product exists in the UI.
    If not present, create it as admin before tests.
    """
    # Login as admin
    home_page, admin_page = login_as_admin(page=page)

    # Check existing products
    existing_products = admin_page.get_current_product_count()
    if product_name in existing_products:
        print(f"ℹ️ Product '{product_name}' already exists, continuing...")
        return admin_page, home_page

    # Otherwise, create product
    admin_page.create_product(product_name)
    print(f"✅ Product '{product_name}' created successfully.")

    return admin_page, home_page



# ----------------------------
# Environment getters
# ----------------------------
def get_backend_url():
    url = os.getenv("BASE_URL_BACKEND")
    if not url:
        raise ValueError("BASE_URL_BACKEND not set in environment or .env")
    return url

def get_frontend_url():
    url = os.getenv("BASE_URL_FRONTEND")
    if not url:
        raise ValueError("BASE_URL_FRONTEND not set in environment or .env")
    return url

def get_admin_credentials():
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    if not username or not password:
        raise ValueError("ADMIN_USERNAME / ADMIN_PASSWORD not found")
    return username, password

def get_user_credentials(user_id: int):
    if user_id == 2:
        username = os.getenv("USERNAME1")
        password = os.getenv("PASSWORD1")
    elif user_id == 3:
        username = os.getenv("USERNAME2")
        password = os.getenv("PASSWORD2")
    else:
        raise ValueError(f"Unknown user_id {user_id}")

    if not username or not password:
        raise ValueError(f"USERNAME{user_id}/PASSWORD{user_id} not found")
    return username, password

# ----------------------------
# Login helpers
# ----------------------------
def login_as_admin(page=None):
    """
    Login as admin; return AdminAPI or page objects if page is passed.
    Automatically creates the first admin if the database is empty.
    """
    # Ensure first admin exists
    ensure_admin_exists()
    
    username, password = get_admin_credentials()
    base_url = get_backend_url()
    token = UserAPI(base_url).login(username, password)
    if not token:
        raise ValueError("Admin login failed, no token returned")

    if page:
        # Lazy import to avoid circular import
        from models.ui.home import HomePage
        from models.ui.admin import AdminPage
        page.add_init_script(f'window.localStorage.setItem("token", "{token}");')
        home_page = HomePage(page)
        home_page.navigate()
        return home_page, AdminPage(page)

    # Lazy import only if page is not provided
    from models.api.admin import AdminAPI
    return AdminAPI(base_url, token=token)


def login_as_user(page=None, user_id: int = 1):
    """Login as user; return UserAPI or page objects if page is passed"""

    # Make sure users 2 and 3 exist before any login
    for uid in (2,3):
        ensure_user_exists(user_id=uid)

    # Then continue with login for whichever user_id is requested
    username, password = get_user_credentials(user_id)
    base_url = get_backend_url()

    token = UserAPI(base_url).login(username, password)
    if not token:
        raise ValueError(f"User {user_id} login failed, no token returned")

    # If a Playwright page is provided, inject token and return UI objects
    if page:
        from models.ui.home import HomePage
        from models.ui.user import UserPage
        page.add_init_script(f'window.localStorage.setItem("token", "{token}");')
        home_page = HomePage(page)
        home_page.navigate()
        return UserPage(page, username), home_page

    return UserAPI(base_url, token=token)