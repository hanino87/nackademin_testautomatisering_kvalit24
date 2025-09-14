import requests
class AdminAPI():
    def __init__(self, base_url,token):
        self.base_url = base_url
        self.token = token
        
    def get_products_list(self):
        """Return the full list of products as dictionaries."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/products", headers=headers)
        return response.json() # convert it to a python dictionare 
        
    def get_current_product_count(self):
        """Return the number of products in the catalog."""
        products = self.get_products_list() # asign variable products to products list wich is a dictonaire 
        return len(products) # return number of products in the list 
        
    def create_product(self, product_name: str):
        """Create a new product in the catalog."""
        headers = {"Authorization": f"Bearer {self.token}"}
        body = {"name": product_name}
        response = requests.post(f"{self.base_url}/products", json=body, headers=headers)
        return response
    
    def search_product_id(self, product_name:str):
     """Search product by id """
     headers = {"Authorization": f"Bearer {self.token}"}
     print(f"DEBUG: Using token = {self.token}")  # Ensure this is a string, not Response object

     response = requests.get(f"{self.base_url}/products", headers=headers)
     print(f"DEBUG: GET /products status code = {response.status_code}")
     print(f"DEBUG: Response JSON = {response.text}")  # full raw JSON

     if response.status_code != 200:
        raise Exception(f"Failed to fetch products: {response.status_code} - {response.text}")

     products = response.json()

     # If API returns a dict with a "products" key
     if isinstance(products, dict) and "products" in products:
        products = products["products"]

     for product in products:
        print(f"DEBUG: Checking product = {product}")  # show each product
        if isinstance(product, dict) and product.get("name") == product_name:
            product_id = product.get("id")
            print(f"DEBUG: Found product ID = {product_id}")
            return product_id

     raise Exception(f"Product '{product_name}' not found")
 
 
    def delete_product_by_name(self, product_name: str):
    # Find the product ID first
     product_id = self.search_product_id(product_name)
     if not product_id:
        raise ValueError(f"Product '{product_name}' not found")

     headers = {"Authorization": f"Bearer {self.token}"}
     response = requests.delete(
        f"{self.base_url}/product/{product_id}",
        headers=headers
    )

     print(f"DEBUG: DELETE /product/{product_id} status = {response.status_code}")
     print(f"DEBUG: DELETE response = {response.text}")

     # Save status_code for later assertions
     self.status_code = response.status_code

     # Ensure deletion succeeded
     assert response.status_code == 200, f"Failed to delete product {product_id}"
     print(f"✅ Deleted product '{product_name}' with ID {product_id}")

     return response.json()
 
    def delete_all_products(self, product_name: str):
        """Delete all products with the given name"""
         # Hitta alla produkt-id:n som matchar namnet
        product_id = self.search_product_id(product_name)
        
        headers = {"Authorization": f"Bearer {self.token}"}
        print(f"DEBUG: Using token = {self.token}") 
        response = requests.delete(
        f"{self.base_url}/product/{product_id}",
        headers=headers)
        # Om search_product_id returnerar en lista
        if not product_id:
         return  # inget att ta bort

        # Ta bort alla produkter som matchar
        for product_id in product_id:
           self.products = [p for p in self.products if p["id"] != product_id]
        print(f"DEBUG: DELETE /product/{product_id} status = {response.status_code}")
        print(f"DEBUG: DELETE response = {response.text}")
        
        # assert deletion of all products 
        assert response.status_code == 200, f"Failed to delete product {product_id}"
        print(f"✅ Deleted product '{product_name}' with ID {product_id}")
        
      
    



        

       

