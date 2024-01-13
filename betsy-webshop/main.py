# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
#-------------------- ALL IMPORTS --------------------
from models import User, Tag, Product, Transaction, create_models
from my_database import db
from random import randint
#------------------- End of imports -------------------

def search(term):
    """
    
        Search for products based on a term in the name or description.

        Parameters:
        - term (str): The search term.

        Returns:
        - None
    """
    # Implement search functionality
    term_lower = term.lower()
    results = (
        Product.select() # select query in peewee
        # selects rows where column 'name' or 'description' -> contains value that contains whatever 'term_lower' is.
        .where((Product.name ** f"%{term_lower}%") | (Product.description ** f"%{term_lower}%"))
    )
    
    print(f"Search results for term '{term}':")
    print(f"results =>\n{results}")
    
    for result in results:
        print(f"result: {result}\n==========\n\n")
        print(f"Product: {result.name}, Description: {result.description}")

def list_user_products(user_id):
    # TODO: Implement listing user products
    pass

def list_products_per_tag(tag_id):
    # TODO: Implement listing products per tag
    pass

def add_product_to_catalog(user_id, product):
    # TODO: Implement adding a product to a user
    pass

def update_stock(product_id, new_quantity):
    # TODO: Implement updating stock quantity of a product
    pass

def purchase_product(product_id, buyer_id, quantity):
    # TODO: Implement handling a purchase
    pass

def remove_product(product_id):
    # TODO: Implement removing a product from a user
    pass


def populate_test_database():
   # Create users
    user_data = [
        {"name": "John Doe", "address": "123 Main St, City1, Country1", "billing_info": "1234-5678-9012-3456"},
        {"name": "Jane Doe", "address": "456 Oak St, City2, Country2", "billing_info": "9876-5432-1098-7654"},
        {"name": "Alice Smith", "address": "789 Elm St, City3, Country3", "billing_info": "5678-9012-3456-7890"},
        {"name": "Bob Johnson", "address": "234 Pine St, City4, Country4", "billing_info": "4321-8765-0987-6543"},
        {"name": "Eva White", "address": "567 Maple St, City5, Country5", "billing_info": "8765-4321-5678-9012"},
        {"name": "Charlie Brown", "address": "890 Birch St, City6, Country6", "billing_info": "3456-7890-1234-5678"},
        {"name": "Olivia Miller", "address": "123 Cedar St, City7, Country7", "billing_info": "6543-2109-8765-4321"},
        {"name": "David Wilson", "address": "456 Walnut St, City8, Country8", "billing_info": "2345-6789-0123-4567"},
        {"name": "Sophia Davis", "address": "789 Spruce St, City9, Country9", "billing_info": "7890-1234-5678-9012"},
        {"name": "Michael Taylor", "address": "234 Pine St, City10, Country10", "billing_info": "4567-8901-2345-6789"},
    ]
    users = [User.get_or_create(name=data["name"], defaults=data)[0] for data in user_data] 

    # Create tags
    tag_data = [
        {"name":"Casual Wear"},
        {"name":"Winter Fashion"},
        {"name":"Outdoor Apparel"},
        {"name":"Stylish Outfits"},
        {"name":"Everyday Essentials"},
    ]
    # get_or_creat -> checks if name in tag_data already exists in db, and if it doesn't exist, 
    # it creates a new one with the provided defaults. [0]-> this is returned instance of the model (in this case Tag model) 
    tags = [Tag.get_or_create(name=data["name"], defaults=data)[0] for data in tag_data]

    # Create products
    product_data = [
        {"name": "Cotton T-shirt", "description": "Comfortable cotton t-shirt for everyday wear", "price": 19.99, "quantity": 50, "owner": users[0], "tags": tags[2]},
        {"name": "Denim Jeans", "description": "Classic denim jeans for a casual look", "price": 39.99, "quantity": 30, "owner": users[1], "tags": tags[3]},
        {"name": "Running Shoes", "description": "Lightweight running shoes for sports and fitness", "price": 59.99, "quantity": 20, "owner": users[2], "tags": tags[2]},
        {"name": "Winter Jacket", "description": "Warm winter jacket for cold weather", "price": 79.99, "quantity": 40, "owner": users[3], "tags": tags[3]},
        {"name": "Formal Shirt", "description": "Formal shirt for professional occasions", "price": 49.99, "quantity": 25, "owner": users[4], "tags": tags[2]},
        {"name": "Sweater - Wool Blend", "description": "Warm wool blend sweater for cold days", "price": 49.99, "quantity": 20, "owner": users[0], "tags": tags[2]},
        {"name": "Leather Jacket", "description": "Stylish leather jacket for a fashionable look", "price": 89.99, "quantity": 15, "owner": users[1], "tags": tags[3]},
        {"name": "Sweater Dress", "description": "Comfortable sweater dress for a cozy style", "price": 69.99, "quantity": 18, "owner": users[2], "tags": tags[2]},
        {"name": "Chino Pants", "description": "Classic chino pants for a versatile wardrobe", "price": 34.99, "quantity": 25, "owner": users[3], "tags": tags[3]},
        {"name": "Hiking Boots", "description": "Durable hiking boots for outdoor adventures", "price": 79.99, "quantity": 30, "owner": users[4], "tags": tags[2]},
    ]
    products = [Product.get_or_create(name=data["name"], defaults=data)[0] for data in product_data]

    # Create transactions
    transaction_data = [
            {"buyer": users[0], "product": products[0], "quantity": randint(1, 5)},
            {"buyer": users[1], "product": products[1], "quantity": randint(1, 5)},
            {"buyer": users[2], "product": products[2], "quantity": randint(1, 5)},
            {"buyer": users[3], "product": products[3], "quantity": randint(1, 5)},
            {"buyer": users[4], "product": products[4], "quantity": randint(1, 5)},
            {"buyer": users[0], "product": products[5], "quantity": randint(1, 5)},
            {"buyer": users[1], "product": products[6], "quantity": randint(1, 5)},
            {"buyer": users[2], "product": products[7], "quantity": randint(1, 5)},
            {"buyer": users[3], "product": products[8], "quantity": randint(1, 5)},
            {"buyer": users[4], "product": products[9], "quantity": randint(1, 5)},
            # Add more transactions as needed
        ]
    transactions = [Transaction.get_or_create(buyer=data["buyer"], product=data["product"], defaults=data)[0] for data in transaction_data]    

def main():
   with db:
       # Create tables if they don't exist
        create_models()
        
        # Create data for testing
        populate_test_database()
        
        # Execute operations
        search("sweater")     
    
if __name__ == "__main__":
    main()
    # print(f"This module contains main logic of this application.")
    