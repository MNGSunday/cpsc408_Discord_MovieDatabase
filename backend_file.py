from helper import helper
from db_operations import db_operations
# python backend_file.py

db_ops = db_operations()

# code for importing the data from the csv files

# Printing records for all tables
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

    # Optional limit to how many entries user views
    print("How many entries would you like returned?")
    print("Enter 1, 5, or 0 for all entries")
    number = helper.get_choice([1,5,0])

    # Obtain appropriate query for specific table based on user choice
    if table_choice == 1:
        query = '''
        SELECT *
        FROM movies
        ORDER BY RAND()
        '''
    if table_choice == 2:
        query = '''
        SELECT *
        FROM actors
        ORDER BY RAND()
        '''
    if table_choice == 3:
        query = '''
        SELECT *
        FROM movieActor
        ORDER BY RAND()
        '''
    if table_choice == 4:
        query = '''
        SELECT *
        FROM directors
        ORDER BY RAND()
        '''
    if table_choice == 5:
        query = '''
        SELECT *
        FROM composers
        ORDER BY RAND()
        '''
    if table_choice == 6:
        query = '''
        SELECT *
        FROM songs
        ORDER BY RAND()
        '''
    if table_choice == 7:
        query = '''
        SELECT *
        FROM studios
        ORDER BY RAND()
        '''
    if table_choice == 8:
        query = '''
        SELECT *
        FROM reviews
        ORDER BY RAND()
        '''

    if number != 0:
        query += "LIMIT:lim"
        dict = {}
        dict["lim"] = number
        results = db_ops.name_placeholder_query(query, dict)
        helper.pretty_print(results)
    else:
        # implement variation of fetchall without need for dictionary
        print("WIP")