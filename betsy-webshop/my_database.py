#-------------------- ALL IMPORTS --------------------
from peewee import SqliteDatabase
#------------------- End of imports -------------------


database = 'betsy.db'
db = SqliteDatabase(database)



############# End Of All Operations ############# 
if __name__ == "__main__":
    print(f"This module contains only database related functions and variables."
    f"\nOnly to be imported and NOT to be executed!!")