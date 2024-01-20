# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
#-------------------- ALL IMPORTS --------------------
from helpers import *
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
        products = Product.select().where(Product.owner == user)

        if products:
            print(f"Products owned by {user.name}:")
            for product in products:
                print(f"Product: {product.name}, Description: {product.description}")
        else:
            print(f"{user.name} does not own any products.")
    else:
        print(f"Can't find any user with this id-nr: {user_id}")

    
    
    
    # user = User.get_or_none(User.id == user_id)
    # products = Product.select().where(Product.owner == user)
    
    # if user and user is not None:
    #     if products and products is not {}:
    #         products = user.products
    #         print(f"Products owned by {user.name}:")
    #         for product in products:
    #             print(f"Product: {product.name}, Description: {product.description}")
    #     else:
    #         print(f"Can't find any products for: {user.name}")
    # else:
    #     print(f"Can't find any user with this id-nr: {user_id}")
    
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

def purchase_product(product_id: int, buyer_id: int, quantity: int):
    print(f"\n-------- Result of purchase_product() function ----------\n")
    buyer = User.get_or_none(User.id == buyer_id)
    product = Product.get_or_none(Product.id == product_id)
    
    if buyer and buyer is not None:
        if product and product is not None:
            if product.quantity >= quantity:
                with db.atomic():
                    transaction = Transaction.create(
                        buyer=buyer,
                        product=product,
                        quantity=quantity
                    )
                    product.quantity -= quantity
                    product.save()

                    # Update the ownership of the product to the buyer
                    product.owner = buyer
                    product.save()

                return (f"Purchase was successful!\n"
                        f"{quantity} units of '{product.name}' were bought by '{buyer.name}'.\n"
                        f"Transaction id: {transaction}")
            else:
                return (f"Purchase failed.\n"
                        f"Insufficient stock for product '{product.name}'.\n"
                        f"Available amount in stock: {product.quantity}.")
        else:
            return (f"Can't find any product with this id: {product_id}")
    else:
        return (f"Can't find any user with this id: {buyer_id}")

    print()
    print(f"=="*30)

def remove_product(product_id):
    print(f"\n-------- Result of remove_product() function ----------\n")
    
    
    print()
    print(f"=="*30)

    

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
        # ========= Testing function: purchase_product() =========
        # purchase_product(7, 5, 3)
        """
        print(purchase_product(73, 5, 1))
        
        
if __name__ == "__main__":
    main()
    