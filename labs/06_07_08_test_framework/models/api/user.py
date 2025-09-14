# View where an user (non admin) can Choose
# produts from the Product Catalog and/or
# remove it
import os
import requests


class UserAPI():
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None # None so the token dont owerwrite in the test 
        
    def login(self, username: str, password: str):
        """ Login metod"""
        body = {"username": username, "password": password}
        response = requests.post(f"{self.base_url}/login", json=body)
        if response.status_code == 200:
           data = response.json()
           self.token = data["access_token"]
           return self.token # return jwt token if dont do this i just return token response 200 could make my other request fail 
        return response
        
    def signup(self, username:str, password:str):
        """singup as a not admin user the signup for admin does in swagger or postman """
        body = {"username": username, "password": password}
        response = requests.post(f"{self.base_url}/signup", json=body)
        return response
    
    def get_user_profile(self):
        """get user loged in profile"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response=requests.get(f"{self.base_url}/user",headers=headers) # store it in an variable the response 
        return response 
        
    def get_user_all_products(self):
        """get users all product"""
        headers = {"Authorization": f"Bearer {self.token}"} # asign respons in header to be used in the request 
        response = requests.get(f"{self.base_url}/user", headers=headers)
        return response.json() # return as python dictionarie to loop through in a later stage 
    
    def search_for_product_id_in_product_list(self, product_name: str):
        """Return product ID by name"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/products", headers=headers)
        data = response.json() # decode json response to a python object so you can iterate throught that object 
        products = data.get("products", [])  # Make sure to access the nested list
        for p in products:
          if p.get("name") == product_name:
            return p.get("id")
        return None

                
    def add_product_to_user(self, product_name:str):
       """add a product to the user"""
       # add product_id variable to matching name from the product list metod for id 
       product_id=self.search_for_product_id_in_product_list(product_name)
       # Step 2: Add that product to the current user
       headers = {"Authorization": f"Bearer {self.token}"}
       response = requests.post(f"{self.base_url}/user/products{product_id}", headers=headers)
       return response.json()
        
        
    def remove_product_from_user(self, product_name:str):
        """remove a product to the user"""
        product_id=self.search_for_product_id_in_product_list(product_name)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}/user/products{product_id}", headers=headers)
        return response.json()

        
        
