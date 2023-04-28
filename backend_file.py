from helper import helper
from db_operations import db_operations
import pandas as pd
# python backend_file.py

# Create db_ops object
db_ops = db_operations()

# -------------------------------------------------
# Code for initializing the data from the csv files

# Clean the sample data files 
#NOTE: Might need to get rid of the header row for each file??? Not sure if that will be an issue
movies_data = pd.read_csv("Test_Data/Movies-TestData.csv")
actors_data = pd.read_csv("Test_Data/Actors-TestData.csv")
movieActors_data = pd.read_csv("Test_Data/MovieActor-TestData.csv")
directors_data = pd.read_csv("Test_Data/Directors-TestData.csv")
composers_data = pd.read_csv("Test_Data/Composers-TestData.csv")
songs_data = pd.read_csv("Test_Data/Songs-TestData.csv")
studios_data = pd.read_csv("Test_Data/Studios-TestData.csv")
reviews_data = pd.read_csv("Test_Data/Reviews-TestData.csv")

# Create the database's tables
db_ops.create_database_tables()
# -------------------------------------------------

#Populates all 8 tables with given sample data
def populate_with_sample_data():
    # insert the data from the csv files
    attribute_count = len(movies_data.columns)
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO Movies VALUES(" + placeholders + ")"
    movies_bulk_data = list(movies_data.itertuples(index=False, name=None))
    db_ops.bulk_insert(query, movies_bulk_data)

    attribute_count = len(actors_data.columns)
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO Actors VALUES(" + placeholders + ")"
    actors_bulk_data = list(actors_data.itertuples(index=False, name=None))
    db_ops.bulk_insert(query, actors_bulk_data)

    attribute_count = len(movieActors_data.columns)
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO MovieActors VALUES(" + placeholders + ")"
    movieActors_bulk_data = list(movieActors_data.itertuples(index=False, name=None))
    db_ops.bulk_insert(query, movieActors_bulk_data)

    attribute_count = len(directors_data.columns)
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO Directors VALUES(" + placeholders + ")"
    directors_bulk_data = list(directors_data.itertuples(index=False, name=None))
    db_ops.bulk_insert(query, directors_bulk_data)

    attribute_count = len(composers_data.columns)
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO Composers VALUES(" + placeholders + ")"
    composers_bulk_data = list(composers_data.itertuples(index=False, name=None))
    db_ops.bulk_insert(query, composers_bulk_data)

    attribute_count = len(songs_data.columns)
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO Songs VALUES(" + placeholders + ")"
    songs_bulk_data = list(songs_data.itertuples(index=False, name=None))
    db_ops.bulk_insert(query, songs_bulk_data)    

    attribute_count = len(studios_data.columns)
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO Studios VALUES(" + placeholders + ")"
    studios_bulk_data = list(studios_data.itertuples(index=False, name=None))
    db_ops.bulk_insert(query, studios_bulk_data)  

    attribute_count = len(reviews_data.columns)
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO Reviews VALUES(" + placeholders + ")"
    reviews_bulk_data = list(reviews_data.itertuples(index=False, name=None))
    db_ops.bulk_insert(query, reviews_bulk_data)  

    print("Sample data has been inserted correctly")

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
        FROM Movies
        ORDER BY RAND()
        '''
    if table_choice == 2:
        query = '''
        SELECT *
        FROM Actors
        ORDER BY RAND()
        '''
    if table_choice == 3:
        query = '''
        SELECT *
        FROM MovieActors
        ORDER BY RAND()
        '''
    if table_choice == 4:
        query = '''
        SELECT *
        FROM Directors
        ORDER BY RAND()
        '''
    if table_choice == 5:
        query = '''
        SELECT *
        FROM Composers
        ORDER BY RAND()
        '''
    if table_choice == 6:
        query = '''
        SELECT *
        FROM Songs
        ORDER BY RAND()
        '''
    if table_choice == 7:
        query = '''
        SELECT *
        FROM Studios
        ORDER BY RAND()
        '''
    if table_choice == 8:
        query = '''
        SELECT *
        FROM Reviews
        ORDER BY RAND()
        '''

    # If user requested to view only a certain amount of results
    if number != 0:
        query += "LIMIT:lim"
        dict = {}
        dict["lim"] = number
        results = db_ops.name_placeholder_query(query, dict)
        helper.pretty_print(results)
    # If user wanted to view all results
    else:
        results = db_ops.query_all_values(query)
        helper.pretty_print(results)


# MAIN CODE:
populate_with_sample_data()

db_ops.destructor()
