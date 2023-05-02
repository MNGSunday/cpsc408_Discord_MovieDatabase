from helper import helper
from db_operations import db_operations
import pandas as pd

# python backend_file.py

# Create db_ops object
db_ops = db_operations()

# -------------------------------------------------
# Code for initializing the data from the csv files

# Clean the sample data files
test_data = {
    "Actors": pd.read_csv("Test_Data/Actors-TestData.csv"),
    "MovieActors": pd.read_csv("Test_Data/MovieActor-TestData.csv"),
    "Directors": pd.read_csv("Test_Data/Directors-TestData.csv"),
    "Composers": pd.read_csv("Test_Data/Composers-TestData.csv"),
    "Studios": pd.read_csv("Test_Data/Studios-TestData.csv"),
    "Movies": pd.read_csv("Test_Data/Movies-TestData.csv"),
    "Songs": pd.read_csv("Test_Data/Songs-TestData.csv"),
    "Reviews": pd.read_csv("Test_Data/Reviews-TestData.csv"),
}

# Create the database's tables
db_ops.create_database_tables()
# -------------------------------------------------

# Populates all 8 tables with given sample data
def populate_with_sample_data():
    relations = [
        "Actors",
        "Directors",
        "Composers",
        "Studios",
        "Movies",
        "MovieActors",
        "Songs",
        "Reviews",
    ]
    for table_name in relations:
        print(table_name)
        data_df = test_data[table_name]
        attribute_count = len(data_df.columns)
        placeholders = ("%s," * attribute_count)[:-1]
        query = f"INSERT INTO {table_name} VALUES({placeholders})"
        bulk_data = list(data_df.itertuples(index=False, name=None))
        db_ops.bulk_insert(query, bulk_data)

    print("Sample data has been inserted correctly")


# Printing records for all tables
def print_table():
    print(
        """Which table would you like to read records from?
    1 - Movies
    2 - Actors
    3 - MovieActors
    4 - Directors
    5 - Composers
    6 - Songs
    7 - Studios
    8 - Reviews
    """
    )
    table_choice = helper.get_choice([1, 2, 3, 4, 5, 6, 7, 8])

    # Optional limit to how many entries user views
    print("How many entries would you like returned?")
    print("Enter 1, 5, or 0 for all entries")
    number = helper.get_choice([1, 5, 0])

    # Obtain appropriate query for specific table based on user choice
    if table_choice == 1:
        query = """
        SELECT *
        FROM Movies
        ORDER BY RAND()
        """
    if table_choice == 2:
        query = """
        SELECT *
        FROM Actors
        ORDER BY RAND()
        """
    if table_choice == 3:
        query = """
        SELECT *
        FROM MovieActors
        ORDER BY RAND()
        """
    if table_choice == 4:
        query = """
        SELECT *
        FROM Directors
        ORDER BY RAND()
        """
    if table_choice == 5:
        query = """
        SELECT *
        FROM Composers
        ORDER BY RAND()
        """
    if table_choice == 6:
        query = """
        SELECT *
        FROM Songs
        ORDER BY RAND()
        """
    if table_choice == 7:
        query = """
        SELECT *
        FROM Studios
        ORDER BY RAND()
        """
    if table_choice == 8:
        query = """
        SELECT *
        FROM Reviews
        ORDER BY RAND()
        """

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


# Filtering options menu
def filter_menu():
    print(
        """Which table would you like to read filtered records from?
        1 - Movies
        2 - Actors
        3 - Directors
        4 - Composers
        5 - Songs
        6 - Reviews
        """
    )
    table_choice = helper.get_choice([1, 2, 3, 4, 5, 6])

    # Optional limit to how many entries user views
    print("How many entries would you like returned?")
    print("Enter 1, 5, or 0 for all entries")
    number = helper.get_choice([1, 5, 0])

    if table_choice == 1:
        filter_movies(number)
    if table_choice == 2:
        filter_actors(number)
    if table_choice == 3:
        filter_directors(number)
    if table_choice == 4:
        filter_composers(number)
    if table_choice == 5:
        filter_songs(number)
    if table_choice == 6:
        filter_reviews(number)


# Filtering options for Movies, variable entry_choice is the number of entries that the user wants returned
def filter_movies(entry_choice):
    print(
        "What would you like to filter results by: Genre, Budget, Average CriticScore, or Average ViewerScore?"
    )
    filter_choice = helper.get_choice_string(
        ["Genre", "Budget", "Average CriticScore", "Average ViewerScore"]
    )

    # User wants to filter movies by genre
    if filter_choice == "Genre":
        genre_query = """
        SELECT DISTINCT genre
        FROM Movies;
        """
        # Show user genres in database, then get their input
        print("Genres from Movie database: ")
        genres = db_ops.single_attribute(genre_query)

        choices = {}
        for i in range(len(genres)):
            print(i, genres[i])
            choices[i] = genres[i]
        index = helper.get_choice(choices.keys())

        query = """
        SELECT name
        FROM Movies
        WHERE genre =:selection
        ORDER BY RANDOM()
        """
        dictionary = {"selection": choices[index]}
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            query += "LIMIT:lim"
            dictionary["lim"] = entry_choice
        results = db_ops.name_placeholder_query(query, dictionary)
        helper.pretty_print(results)

    # User wants to filter movies by budget
    if filter_choice == "Budget":
        print(
            """What would you like to filter movie results by?
        1 - Budget over 100,000,000
        2 - Budget under 100,000,000
        """
        )
        budget_choice = helper.get_choice([1, 2])

        if budget_choice == 1:
            query = """
            SELECT name
            FROM Movies
            WHERE budget > 100000000
            ORDER BY RANDOM()
            """
        else:
            query = """
            SELECT name
            FROM Movies
            WHERE budget < 100000000
            ORDER BY RANDOM()
            """
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            query += "LIMIT:lim"
            dict = {}
            dict["lim"] = entry_choice
            results = db_ops.name_placeholder_query(query, dict)
            helper.pretty_print(results)
        else:
            results = db_ops.query_all_values(query)
            helper.pretty_print(results)

    # User wants to filter movies by Average Critic Score
    if filter_choice == "Average CriticScore":
        print(
            """What would you like to filter movie results by?
            1 - Average Critic Score over 65
            2 - Average Critic Score under 65
            """
        )
        critic_choice = helper.get_choice([1, 2])

        if critic_choice == 1:
            query = """
            SELECT name
            FROM Movies
            WHERE criticScore > 65
            ORDER BY RANDOM()
            """
        else:
            query = """
            SELECT name
            FROM Movies
            WHERE criticScore < 65
            ORDER BY RANDOM()
            """
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            query += "LIMIT:lim"
            dict = {}
            dict["lim"] = entry_choice
            results = db_ops.name_placeholder_query(query, dict)
            helper.pretty_print(results)
        else:
            results = db_ops.query_all_values(query)
            helper.pretty_print(results)

    # User wants to filter movies by Average Viewer Score
    if filter_choice == "Average ViewerScore":
        print(
            """What would you like to filter movie results by?
            1 - Average Viewer Score over 65
            2 - Average Viewer Score under 65
            """
        )
        viewer_choice = helper.get_choice([1, 2])

        if viewer_choice == 1:
            query = """
            SELECT name
            FROM Movies
            WHERE viewerScore > 65
            ORDER BY RANDOM()
            """
        else:
            query = """
            SELECT name
            FROM Movies
            WHERE viewerScore < 65
            ORDER BY RANDOM()
            """
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            query += "LIMIT:lim"
            dict = {}
            dict["lim"] = entry_choice
            results = db_ops.name_placeholder_query(query, dict)
            helper.pretty_print(results)
        else:
            results = db_ops.query_all_values(query)
            helper.pretty_print(results)


# Filtering options for Actors, variable entry_choice is the number of entries that the user wants returned
def filter_actors(entry_choice):
    print(
        """You have the following options for filtering Actors:
    1 - Actors under 65
    2 - Actors over 65
    3 - Youngest to Oldest
    """
    )
    filter_choice = helper.get_choice([1, 2, 3])
    if filter_choice == 1:
        query = """
        SELECT name
        FROM Actors
        WHERE age < 65
        ORDER BY RANDOM()
        """
    elif filter_choice == 2:
        query = """
        SELECT name
        FROM Actors
        WHERE age > 65
        ORDER BY RANDOM()
        """
    else:
        query = """
        SELECT name
        FROM Actors
        ORDER BY age DESC
        """

    # User wanted only 1 or 5 results
    if entry_choice != 0:
        query += "LIMIT:lim"
        dict = {}
        dict["lim"] = entry_choice
        results = db_ops.name_placeholder_query(query, dict)
        helper.pretty_print(results)
    else:
        results = db_ops.query_all_values(query)
        helper.pretty_print(results)


# Filtering options for Directors, variable entry_choice is the number of entries that the user wants returned
def filter_directors(entry_choice):
    print(
        """You have the following options for filtering Directors:
    1 - Directors under 65
    2 - Directors over 65
    3 - Youngest to Oldest
    """
    )
    filter_choice = helper.get_choice([1, 2, 3])
    if filter_choice == 1:
        query = """
        SELECT name
        FROM Directors
        WHERE age < 65
        ORDER BY RANDOM()
        """
    elif filter_choice == 2:
        query = """
        SELECT name
        FROM Directors
        WHERE age > 65
        ORDER BY RANDOM()
        """
    else:
        query = """
        SELECT name
        FROM Directors
        ORDER BY age DESC
        """

    # User wanted only 1 or 5 results
    if entry_choice != 0:
        query += "LIMIT:lim"
        dict = {}
        dict["lim"] = entry_choice
        results = db_ops.name_placeholder_query(query, dict)
        helper.pretty_print(results)
    else:
        results = db_ops.query_all_values(query)
        helper.pretty_print(results)


# Filtering options for Composers, variable entry_choice is the number of entries that the user wants returned
def filter_composers(entry_choice):
    print(
        """You have the following options for filtering Composers:
    1 - Composers under 65
    2 - Composers over 65
    3 - Composed for under 50 movies
    4 - Composed for over 50 movies
    """
    )
    filter_choice = helper.get_choice([1, 2, 3])
    if filter_choice == 1:
        query = """
        SELECT name
        FROM Composers
        WHERE age < 65
        ORDER BY RANDOM()
        """
    elif filter_choice == 2:
        query = """
        SELECT name
        FROM Composers
        WHERE age > 65
        ORDER BY RANDOM()
        """
    elif filter_choice == 3:
        query = """
        SELECT name
        FROM Composers
        WHERE movieCount < 50
        ORDER BY RANDOM()
        """
    else:
        query = """
        SELECT name
        FROM Composers
        WHERE movieCount > 50
        ORDER BY RANDOM()
        """

    # User wanted only 1 or 5 results
    if entry_choice != 0:
        query += "LIMIT:lim"
        dict = {}
        dict["lim"] = entry_choice
        results = db_ops.name_placeholder_query(query, dict)
        helper.pretty_print(results)
    else:
        results = db_ops.query_all_values(query)
        helper.pretty_print(results)


# Filtering options for Songs, variable entry_choice is the number of entries that the user wants returned
def filter_songs(entry_choice):
    print(
        """You have the following options for filtering Songs:
    1 - Songs shorter than 150 seconds
    2 - Songs longer than 150 seconds
    """
    )
    filter_choice = helper.get_choice([1, 2])

    if filter_choice == 1:
        query = """
        SELECT songName
        FROM Songs
        WHERE songLength < 150
        ORDER BY RANDOM()
        """
    else:
        query = """
        SELECT songName
        FROM Songs
        WHERE songLength > 150
        ORDER BY RANDOM()
        """
    # User wanted only 1 or 5 results
    if entry_choice != 0:
        query += "LIMIT:lim"
        dict = {}
        dict["lim"] = entry_choice
        results = db_ops.name_placeholder_query(query, dict)
        helper.pretty_print(results)
    else:
        results = db_ops.query_all_values(query)
        helper.pretty_print(results)


# Filtering options for Reviews, variable entry_choice is the number of entries that the user wants returned
def filter_reviews(entry_choice):
    print(
        """You have the following options for filtering Reviews:
    1 - Find reviews by Movie Name
    2 - Find Movie reviews scoring > 7.5 on a scale of 0 to 11
    3 - Find Movie reviews scoring < 7.5 on a scale of 0 to 11
    """
    )
    filter_choice = helper.get_choice([1, 2, 3])

    if filter_choice == 1:
        name_query = """
        SELECT DISTINCT name
        FROM Movies;
        """
        # Show user movie names in database, then get their input
        print("Names from Movie database: ")
        names = db_ops.single_attribute(name_query)

        choices = {}
        for i in range(len(names)):
            print(i, names[i])
            choices[i] = names[i]
        name_index = helper.get_choice(choices.keys())

        query = """
        SELECT Movies.name, Reviews.username, Reviews.text
        FROM Reviews
        INNER JOIN Movies ON Movies.movieID = Reviews.movieID
        WHERE Movies.name =:selection
        ORDER BY RANDOM()
        """
        dictionary = {"selection": choices[name_index]}
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            query += "LIMIT:lim"
            dictionary["lim"] = entry_choice
        results = db_ops.name_placeholder_query(query, dictionary)
        helper.pretty_print(results)

    else:
        if filter_choice == 2:
            query = """
            SELECT Movies.name, Reviews.username, Reviews.text
            FROM Reviews
            INNER JOIN Movies ON Movies.movieID = Reviews.movieID
            WHERE Reviews.score > 7.5
            ORDER BY RANDOM()
            """
        else:
            query = """
            SELECT Movies.name, Reviews.username, Reviews.text
            FROM Reviews
            INNER JOIN Movies ON Movies.movieID = Reviews.movieID
            WHERE Reviews.score < 7.5
            ORDER BY RANDOM()
            """
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            query += "LIMIT:lim"
            dict = {}
            dict["lim"] = entry_choice
            results = db_ops.name_placeholder_query(query, dict)
            helper.pretty_print(results)
        else:
            results = db_ops.query_all_values(query)
            helper.pretty_print(results)

# HAS NOT BEEN TESTED
# Picks a random movie for the user to watch
def randomMoviePicker():
    query = '''
    SELECT Name, Runtime, Genre
    FROM Movies
    ORDER BY RANDOM()
    LIMIT 1
    '''

    results = db_ops.whole_record(query)

    print("Here's what you'll be watching tonight!\n")
    print("   Title     |  Runtime |    Genre   ")
    helper.pretty_print(results)

# HAS NOT BEEN TESTED
# Allows a user to add a movie to the database
def addMovie():
    # This function is SUCH A MESS I'm so sorry to whoever sees this. I can try
    # to make it cleaner later :(

    # Booleans to control whether we add new entries to other tables or not:
    newDirector = True
    newComposer = True
    newStudio = True

    # Movie: MovieID,Name,DirectorID,ComposerID,StudioID,Runtime,Budget,GrossProfit,CriticScore,ViewerScore,Genre,Year,NominatedForAward,PSafeRating
    movieTitle = input("Enter the name of the film: ")
    runtime = int(input("Enter the runtime: "))
    budget = int(input("Enter the budget: "))
    grossProfit = int(input("Enter the gross profit: "))
    criticScore = int(input("Enter the critic score: "))
    viewerScore = int(input("Enter the viewer score: "))
    genre = input("Enter the genre: ")
    year = int(input("Enter the year: "))
    movieNomForAward = input("Was the film nominated for an award? True/False: ")
    pSafeRating = input("Enter the P Safe Rating: ")

    # Director: DirectorID,Name,Age
    directorName = input("Enter the director's name: ")

    # AT THIS POINT, CHECK IF WE ALREADY HAVE THAT DIRECTOR BEFORE PROCEEDING
    queryX = '''
    SELECT DISTINCT Name
    FROM Directors;
    '''
    #Gets a list of all director names and see if we already have it
    directorNames = db_ops.single_attribute(queryX)
    for dirName in directorNames:
        if (directorName == dirName):
            newDirector = False

    # Make the new entry
    if (newDirector):
        directorAge = int(input("Enter the director's age: "))
        
        # Insert the new director as a record
        queryDir = '''
        INSERT INTO Directors (Name, Age)
        '''
        queryDir += "VALUES ({directorName}, {directorAge})"
        db_ops.insert_single_record(queryDir)


    # Composer: ComposerID,Name,Age,MovieCount
    composerName = input("Enter the composer's name: ")

    # AT THIS POINT, CHECK IF WE ALREADY HAVE THAT COMPOSER BEFORE PROCEEDING
    queryY = '''
    SELECT DISTINCT Name
    FROM Composers;
    '''
    #Gets a list of all director names and see if we already have it
    composerNames = db_ops.single_attribute(queryY)
    for comName in composerNames:
        if (composerName == comName):
            newComposer = False

    # Add the new entry
    if (newComposer):
        composerAge = int(input("Enter the composer's age: "))
        composerMovieCount = int(input("Enter the number of movies the composer has composed for: "))
       
        # Insert the new composer as a record
        queryCom = '''
        INSERT INTO Composers (Name, Age, MovieCount)
        '''
        queryCom += "VALUES ({composerName}, {composerAge}, {composerMovieCount})"
        db_ops.insert_single_record(queryCom)


    # Studio: StudioID,Name,Location
    studioName = input("Enter the studio's name: ")

    # AT THIS POINT, CHECK IF WE ALREADY HAVE THAT STUDIO BEFORE PROCEEDING
    queryZ = '''
    SELECT DISTINCT Name
    FROM Studios;
    '''
    #Gets a list of all director names and see if we already have it
    studioNames = db_ops.single_attribute(queryZ)
    for stuName in studioNames:
        if (studioName == stuName):
            newStudio = False

    # Add the new entry
    if (newStudio):
        studioLocation = input("Enter the studio's location: ")
       
        # Insert the new studio as a record
        queryStu = '''
        INSERT INTO Studios (Name, Location)
        '''
        queryStu += "VALUES ({studioName}, {studioLocation})"
        db_ops.insert_single_record(queryStu)


    # Now that any new entries into other tables have been added, we can add the movie
    # First, get the IDs of the director, composer, and studio
    #Director:
    query = '''
    SELECT DirectorID
    FROM Directors
    WHERE Name = {directorName}
    '''
    dIDList = db_ops.single_attribute(query)
    dirID = dIDList[0]

    #Composer:
    query = '''
    SELECT ComposerID
    FROM Composers
    WHERE Name = {composerName}
    '''
    cIDList = db_ops.single_attribute(query)
    comID = cIDList[0]

    #Studio:
    query = '''
    SELECT StudioID
    FROM Studios
    WHERE Name = {studioName}
    '''
    sIDList = db_ops.single_attribute(query)
    stuID = sIDList[0]


    # Finally, add the movie
    queryMov = '''
    INSERT INTO Movies (Name, DirectorID, ComposerID, StudioID, Runtime, Budget, GrossProfit, CriticScore, ViewerScore, Genre, Year, NominatedForAward, PSafeRating)
    VALUES ({movieTitle}, {dirID}, {comID}, {stuID}, {runtime}, {budget}, {grossProfit}, {criticScore}, {viewerScore}, {genre}, {year}, {movieNomForAward}, {pSafeRating})
    '''
    db_ops.insert_single_record(queryMov)

    print("{movieTitle} has been added to the database!")



# HAS NOT BEEN TESTED
# Allows a user to add an actor to the database
def addActor():
    # This takes the actor's info, adds an entry, then prompts to ask
    # if the actor has been in a movie. If yes, get the name, check with
    # the database, and if that movie exists, make an entry in the
    # MovieActor table
    pass

# HAS NOT BEEN TESTED
# Allows a user to add a song to the database
def addSong():
    # Get the song's title, then composer. If composer doesn't exist yet,
    # get that info first. Then continue with song's info
    pass

# HAS NOT BEEN TESTED
# Allows a user to add a review for an existing movie
def addReview():
    pass

# MAIN CODE:
populate_with_sample_data()

db_ops.destructor()
