from helper import helper
from db_operations import db_operations
# python backend_file.py

db_ops = db_operations()

# code for importing the data from the csv files

def print_table():
    print('''Which table would you like to read records from?
    1 - Movies
    2 - Actors
    3 - MovieActor
    4 - Directors
    5 - Composers
    6 - Songs
    7 - Studios
    8 - Reviews
    ''')
    table_choice = helper.get_choice([1,2,3,4,5,6,7,8])