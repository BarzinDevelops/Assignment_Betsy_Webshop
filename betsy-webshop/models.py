#-------------------- ALL IMPORTS --------------------
import helpers
from peewee import Model, CharField, IntegerField, DecimalField, ForeignKeyField
from peewee import SqliteDatabase
#------------------- End of imports -------------------

# creating the database
database = 'betsy.db'
db = SqliteDatabase(database)

# Models go here

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(unique=True)
    address = CharField()
    billing_info = CharField()

class Tag(BaseModel):
    name = CharField(unique=True)

class Product(BaseModel):
    name = CharField(unique=True)
    description = CharField()
    price = DecimalField(decimal_places=2)  # Using DecimalField for precise decimal storage
    quantity = IntegerField()
    
    owner = ForeignKeyField(User, backref='products')  # Creating a foreign key relationship with User
    tags = ForeignKeyField(Tag, backref='products')  # Creating a foreign key relationship with Tag

class Transaction(BaseModel):
    buyer = ForeignKeyField(User, backref='purchases')
    product = ForeignKeyField(Product, backref='purchases')
    quantity = IntegerField()


def create_models():
    with db:
        db.create_tables([Tag, User, Product, Transaction])
    
if __name__ == "__main__":
    print(f"This module contains only MODELS."
    f"\nOnly to be imported and NOT to be executed!!")
    