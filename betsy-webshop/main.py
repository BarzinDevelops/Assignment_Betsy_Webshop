# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
#-------------------- ALL IMPORTS --------------------
from helpers import *
#------------------- End of imports -------------------

def search(term:str):
    """   
        Search for products based on a term in the name or description and returns 
        a list of the results.

        Parameters:
        - term (str):   The search term (word that could be the name of the product 
                        or a part of its description).
    """
    term_lower = term.lower()
    results = (
        Product.select() # select query in peewee
        # selects rows where column 'name' or 'description' -> contains value that matches whatever 'term_lower' is.
        .where((Product.name ** f"%{term_lower}%") | (Product.description ** f"%{term_lower}%"))
    )
    found_products = []
    for product in results:
       found_products.append({
            "Product ID" : product.id,
            "Product Name" : product.name,
            "Product Description" : product.description
        })
    return found_products
    
def list_user_products(user_id:int):
    """   
        Returns the products of a given user.

        Parameters:
        - user_id (int): Id of the given user.
    """
    user = User.get_or_none(User.id == user_id)
    if user and user is not None:
        products = Product.select().where(Product.owner == user)
        if products:
            users_products = []
            for product in products:
                users_products.append({ 
                    "Owner Name": product.owner.name,
                    "Product ID": product.id,
                    "Product Name": product.name,
                    "Product Description" : product.description
                })
            return users_products
        else:
            return (f"{user.name} does not own any products.")
    else:
        return (f"Can't find any user with this id-nr: {user_id}")

def list_products_per_tag(tag_id:int):
    """   
        Returns all products for a given tag.

        Parameters:
        - tag_id (int): Id of the given tag.
    """
    tag = Tag.get_or_none(Tag.id == tag_id)
    if tag and tag is not None:
        products = tag.products
        matching_products = []
        for product in products:
            matching_products.append({ 
                "Tag ID" : tag.id,
                "Product Name": product.name,
                "Description": product.description
            })
        return matching_products
    else:
        print()
        return [{"ERROR" : f"Nothing found for this tag id: {tag_id}"}]

def add_product_to_catalog(user_id:int, product_to_add:dict):
    """   
        Add a product to a user.
              
        Parameters:
        - user_id (int): Id of the given user.
        - product (dict): Containing columns as keys and their values.
    """
    user = User.get_or_none(User.id == user_id)
    if user and user is not None:
        if product_to_add and product_to_add is not {}:
            new_product, is_created = Product.get_or_create(
                name=product_to_add['name'],
                description=product_to_add['description'],
                price=product_to_add['price'],
                quantity=product_to_add['quantity'],
                owner=user,
                tags=product_to_add['tags']
            , defaults=product_to_add)
            
            if is_created:
                added_product = [
                    {
                        "Added Product ID" : new_product.id,
                        "Added Product Name" : new_product.name,
                        "Added Product With Tag ID" : new_product.tags.id,
                        "Added Product With Tag Name" : new_product.tags.name,
                        "Added Product To Owner ID" : new_product.owner.id,
                        "Added Product To Owner Name" : new_product.owner.name,
                    }
                ]
                return added_product
        else:
            print()
            return [{"ERROR" : f"The product you gave can't be added!\nIt contains this: {product_to_add}"}]
    else:
        print()
        return [{"ERROR" : f"Can't find any user with this id-nr: {user_id}"}]

def update_stock(product_id:int, new_quantity:int): 
    """
        Update the stock quantity of a product.

        Parameters:
        - product_id (int): The ID of the product to update.
        - new_quantity (int): The new quantity to set.
    """
    product = Product.get_or_none(Product.id == product_id)
    if product and product is not None:
        previous_quantity = product.quantity
        product.quantity = new_quantity
        product.save()
        updated_result = [
            {
                "Product Name" : product.name,
                "Previous quantity": previous_quantity,
                "Current quantity": product.quantity
            }
        ]
        return updated_result
    else:
        print()
        return [{"ERROR" : f"Nothing found for this product id: {product_id}"}]

def purchase_product(product_id: int, buyer_id: int, quantity: int):
    """
        Handles a purchase between a buyer and a seller for a given product.

        Parameters:
        - product_id (int): The ID of the product to retrieve.
        - buyer_id (int): The ID of user that purchases the product.
        - quantity (int): The current amount of the product.
    """
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

def remove_product(product_id:int):
    """
    Remove a product from the user.

    Parameters:
    - product_id (int): The ID of the product to remove.
    """
    product = Product.get_or_none(Product.id == product_id)
    if product and product is not None:
        owner = product.owner
        product.delete_instance()
        return (f"Product '{product.name}' is removed from {owner.name}'s catalog.")
    else:
        return (f"Can't find any product with this id: {product_id}")


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
        
if __name__ == "__main__": 
    with db:
        # Create tables if they don't exist
        create_models()
    
    # Create data for testing
    # populate_test_database()
    
    """ Test cases: copy each test case you want from this collection and run it seperately.
        # =========== Testing function: search() ===============   
        print("\n"+"=="*50+"\n")
        [print(f"{property}: {value}") for item in search("sweater") for property, value in item.items()]
        print("\n"+"=="*50+"\n") 
        # =========== Testing function: list_user_products() =============== 
        print("\n"+"=="*50+"\n")
        [print(f"{property}: {value}") for item in list_user_products(1) for property, value in item.items()]
        [print(f"{property}: {value}") for item in list_user_products(31) for property, value in item.items()] # testing with non existing value
        print("\n"+"=="*50+"\n")
        # =========== Testing function: list_products_per_tag() ===============
        prod1_dict = helpers.test_product1_to_add
        prod2_dict = helpers.test_product2_to_add
        print("\n"+"=="*50+"\n")
        [print(f"{property}: {value}") for item in list_products_per_tag(3) for property, value in item.items()]
        [print(f"{property}: {value}") for item in list_products_per_tag(50) for property, value in item.items()]
        print("\n"+"=="*50+"\n")
        # =========== Testing function: add_product_to_catalog() ===============
        print("\n"+"=="*50+"\n")
        add_product_to_catalog(2, {
            "name": "New Product",
            "description": "A fantastic new product",
            "price": 29.99,
            "quantity": 10,
            "tags": 1  # Assuming tag ID 1
        })
        print("\n"+"=="*50+"\n")
        # =========== Testing function: update_stock() ===============
        print("\n"+"=="*50+"\n")
        [print(f"{property}: {value}") for item in update_stock(10, 30) for property, value in item.items()]
        [print(f"{property}: {value}") for item in update_stock(84, 5) for property, value in item.items()]
        print("\n"+"=="*50+"\n")
        # ========= Testing function: purchase_product() =========
        print("\n"+"=="*50+"\n")
        print(purchase_product(73, 5, 1)) # testing with wrong product-id
        print(purchase_product(7, 45, 1)) # testing with wrong user-id
        print(purchase_product(7, 5, 100)) # testing with unavailable amount
        print("\n"+"=="*50+"\n")
    """
    
    # Execute operations

    # =========== Testing function: search() ===============   
    print("\n"+"=="*50+"\n")
    [print(f"{property}: {value}") for item in search("sweater") for property, value in item.items()]
    print("\n"+"=="*50+"\n") 
