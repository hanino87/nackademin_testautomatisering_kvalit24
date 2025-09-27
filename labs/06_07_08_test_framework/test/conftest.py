# test/conftest.py
import os
import pytest

@pytest.fixture(scope="function", autouse=True)
def inject_backend_url(page):
    backend_url = os.environ.get("BASE_URL_BACKEND", "http://app-backend:8000")
    page.add_init_script(f"window.__BASE_URL_BACKEND__ = '{backend_url}';")
