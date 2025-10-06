# lab_06/test/integration/locustfile.py


import random
import string
from locust import HttpUser, task, between


class UserBehavior_Login(HttpUser):
    wait_time = between(1, 2)  # simulate user think time

    def on_start(self):
        """Executed when each simulated user starts"""
        # Generate random username and password
        self.username = "user_" + ''.join(random.choices(string.ascii_lowercase, k=6))
        self.password = "pass_" + ''.join(random.choices(string.ascii_lowercase, k=7))

        # -------------------------
        # Signup
        # -------------------------
        signup_response = self.client.post(
            "/signup",
            json={"username": self.username, "password": self.password}
        )
        self.signup_status = signup_response.status_code  # store for task check
        if signup_response.status_code == 200:
            print(f"✅ Signup succeeded for {self.username}")
        else:
            print(f"⚠️ Signup failed for {self.username}: {signup_response.status_code}")

        # -------------------------
        # Login
        # -------------------------
        login_response = self.client.post(
            "/login",
            json={"username": self.username, "password": self.password}
        )
        if login_response.status_code == 200:
            self.token = login_response.json().get("access_token")
            print(f"✅ Login succeeded for {self.username}")
        else:
            self.token = None
            print(f"⚠️ Login failed for {self.username}: {login_response.status_code}")

    # -------------------------
    # Task to verify signup
    # -------------------------
    @task
    def check_signup(self):
        """Task to verify that the user was successfully registered"""
        if getattr(self, "signup_status", 0) == 200:
            print(f"{self.username} is registered ✅")
        else:
            print(f"{self.username} registration failed ⚠️")

    # -------------------------
    # Task to verify login
    # -------------------------
    @task
    def check_login(self):
        """Task to verify that login succeeded"""
        if getattr(self, "token", None):
            print(f"{self.username} is logged in ✅")
        else:
            print(f"{self.username} login failed ⚠️")
