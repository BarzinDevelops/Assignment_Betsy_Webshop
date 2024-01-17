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
    print(f"\n\n-------- Result of search() function ----------\n")
    # Implement search functionality
    term_lower = term.lower()
    results = (
        Product.select() # select query in peewee
        # selects rows where column 'name' or 'description' -> contains value that matches whatever 'term_lower' is.
        .where((Product.name ** f"%{term_lower}%") | (Product.description ** f"%{term_lower}%"))
    )
    
    for result in results:
        print(f"Product: {result.name}, Description: {result.description}")
    
    print()
    print(f"=="*30)
    
def list_user_products(user_id):
    """   
        View the products of a given user.

        Parameters:
        - user_id (int): Id of the given user.

        Returns:
        - None
    """
    print(f"\n-------- Result of list_user_products() function ----------\n")
    user = User.get_or_none(User.id == user_id)
    if user and user is not None:
        products = user.products
        print(f"Products owned by {user.name}:")
        for product in products:
            print(f"Product: {product.name}, Description: {product.description}")
    else:
        print(f"Can't find any user with this id-nr: {user_id}")
    
    print()
    print(f"=="*30)

def list_products_per_tag(tag_id):
    """   
        View all products for a given tag.

        Parameters:
        - tag_id (int): Id of the given tag.

        Returns:
        - None
    """
    print(f"\n-------- Result of list_products_per_tag() function ----------\n")
    tag = Tag.get_or_none(Tag.id == tag_id)
    if tag_id and tag is not None:
        products = tag.products
        print(f"Products under tag '{tag.name}':\n")
        for product in products:
            print(f" - Product name: {product.name}, Description: {product.description}")
    else:
        print(f"Can't find any tag with this tag-id: {tag_id}")
    
    print()
    print(f"=="*30)

def add_product_to_catalog(user_id, product):
    """   
        Add a product to a user.
        
        Parameters:
        - user_id (int): Id of the given user.
        - product (dict): Containing columns as keys and their values.
        
        Returns:
        - None
    """
    print(f"\n-------- Result of add_product_to_catalog() function ----------\n")
    user = User.get_or_none(User.id == user_id)
    if user and user is not None:
        if product and product is not {}:
            new_product, is_created = Product.get_or_create(
                name=product['name'],
                description=product['description'],
                price=product['price'],
                quantity=product['quantity'],
                owner=user,
                tags=product['tags']
            , defaults=product)
            
            if is_created:
                print(f"This product: {new_product.name} has been added to the database successfullly.")
            else:
                print(f"This product: '{new_product.name}', was already in the database!")
        else:
            print(f"Can't find any product for: {product}.")
    else:
        print(f"Can't find any user with this id-nr: {user_id}")
    
    print()
    print(f"=="*30)

def update_stock(product_id:int, new_quantity:int): 
    """
        Update the stock quantity of a product.

        Parameters:
        - product_id (int): The ID of the product to update.
        - new_quantity (int): The new quantity to set.

        Returns:
        - None
    """
    print(f"\n-------- Result of update_stock() function ----------\n")
    product = Product.get_or_none(Product.id == product_id)
    if product and product is not None:
        product.quantity = new_quantity
        product.save()
        print(f"Stock quantity for product '{product.name}' updated to {new_quantity}.")
    else:
        print(f"Can't find any product with this id: {product_id}")
    
    print()
    print(f"=="*30)

def purchase_product(product_id, buyer_id, quantity):
    print(f"\n-------- Result of purchase_product() function ----------\n")
    
    
    print()
    print(f"=="*30)

def remove_product(product_id):
    print(f"\n-------- Result of remove_product() function ----------\n")
    
    
    print()
    print(f"=="*30)

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

# this is my own function for getting all products etc...
def get_products(prod_id):
    print(f"\n-------- Result of get_products() function ----------\n")
    products = (
        Product.select()
            .where(Product.id.in_(prod_id))
    )
    
    for product in products:
        print(f"This is info on product whith id: {product.id}\n\n"
            f"  product name:           {product.name}\n"
            f"  product description:    {product.description}\n"
            f"  product price:          {product.price}\n"
            f"  product quantity:       {product.quantity}"
        )
    
    print()
    print(f"=="*30)
    
def main():
   with db:
       # Create tables if they don't exist
        create_models()
        
        # Create data for testing
        # populate_test_database()
        
        # Execute operations
        """         
        # =========== Testing function: search() =============== 
        search("sweater")   
        # =========== Testing function: list_user_products() ===============  
        list_user_products(3)
        list_user_products(100) # testing with non existing value
        # =========== Testing function: list_products_per_tag() ===============
        list_products_per_tag(3)
        list_products_per_t ag(50) # testing with non existing value
        # =========== Testing function: add_product_to_catalog() ===============
        add_product_to_catalog(1, {
            "name": "New Product",
            "description": "A fantastic new product",
            "price": 29.99,
            "quantity": 10,
            "tags": 1  # Assuming tag ID 1
        })
        # =========== Testing function: update_stock() ===============
        print(f"Before running -> update_stock():")
        get_products([11])
        
        update_stock(11, 10)
        
        print(f"After running -> update_stock():")
        get_products([11])
        """
        
        # =========== Testing function: purchase_product() ===============
        
        
        
if __name__ == "__main__":
    main()
    # print(f"This module contains main logic of this application.")
    