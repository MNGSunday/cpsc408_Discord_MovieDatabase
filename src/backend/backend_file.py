from helper import helper
from db_operations import db_operations
import pandas as pd
import mysql.connector

# python backend_file.py

# Create db_ops object
db_ops = db_operations()

# -------------------------------------------------
# Code for initializing the data from the csv files

# Clean the sample data files
test_data = {
    "Actors": pd.read_csv("Actors-TestData.csv"),
    "MovieActors": pd.read_csv("MovieActor-TestData.csv"),
    "Directors": pd.read_csv("Directors-TestData.csv"),
    "Composers": pd.read_csv("Composers-TestData.csv"),
    "Studios": pd.read_csv("Studios-TestData.csv"),
    "Movies": pd.read_csv("Movies-TestData.csv"),
    "Songs": pd.read_csv("Songs-TestData.csv"),
    "Reviews": pd.read_csv("Reviews-TestData.csv"),
}

# Create the database's tables
try:
    db_ops.create_database_tables()
except (mysql.connector.InterfaceError, mysql.connector.errors.ProgrammingError) as e:
    print("Tables already exist. Proceeding as usual...")
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
        # print(table_name)
        data_df = test_data[table_name]
        attribute_count = len(data_df.columns)
        placeholders = ("%s," * attribute_count)[:-1]
        query = f"INSERT INTO {table_name} VALUES({placeholders})"
        bulk_data = list(data_df.itertuples(index=False, name=None))
        db_ops.bulk_insert(query, bulk_data)

    print("Sample data has been inserted correctly")


# Printing records for all tables
def print_menu():
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
        WHERE deleted = 0
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
        WHERE deleted = 0
        ORDER BY RAND()
        """

    # If user requested to view only a certain amount of results
    if number != 0:
        num_string = str(number)
        query += "LIMIT "
        query += num_string
        results = db_ops.query_all_values(query)
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
        WHERE genre = "%s"
        ORDER BY RAND()
        """
        # dictionary = {"selection": choices[index]}
        # print("Selected: ", choices[index])
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
        results = db_ops.query_all_values(query % choices[index])
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
            ORDER BY RAND()
            """
        else:
            query = """
            SELECT name
            FROM Movies
            WHERE budget < 100000000
            ORDER BY RAND()
            """
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
            results = db_ops.query_all_values(query)
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
            ORDER BY RAND()
            """
        else:
            query = """
            SELECT name
            FROM Movies
            WHERE criticScore < 65
            ORDER BY RAND()
            """
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
            results = db_ops.query_all_values()
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
            ORDER BY RAND()
            """
        else:
            query = """
            SELECT name
            FROM Movies
            WHERE viewerScore < 65
            ORDER BY RAND()
            """
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
            results = db_ops.query_all_values(query)
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
        ORDER BY RAND()
        """
    elif filter_choice == 2:
        query = """
        SELECT name
        FROM Actors
        WHERE age > 65
        ORDER BY RAND()
        """
    else:
        query = """
        SELECT name
        FROM Actors
        ORDER BY age ASC
        """

    # User wanted only 1 or 5 results
    if entry_choice != 0:
        lim_string = str(entry_choice)
        query += "LIMIT "
        query += lim_string
        results = db_ops.query_all_values(query)
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
        ORDER BY RAND()
        """
    elif filter_choice == 2:
        query = """
        SELECT name
        FROM Directors
        WHERE age > 65
        ORDER BY RAND()
        """
    else:
        query = """
        SELECT name
        FROM Directors
        ORDER BY age DESC
        """

    # User wanted only 1 or 5 results
    if entry_choice != 0:
        lim_string = str(entry_choice)
        query += "LIMIT "
        query += lim_string
        results = db_ops.query_all_values(query)
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
        ORDER BY RAND()
        """
    elif filter_choice == 2:
        query = """
        SELECT name
        FROM Composers
        WHERE age > 65
        ORDER BY RAND()
        """
    elif filter_choice == 3:
        query = """
        SELECT name
        FROM Composers
        WHERE movieCount < 50
        ORDER BY RAND()
        """
    else:
        query = """
        SELECT name
        FROM Composers
        WHERE movieCount > 50
        ORDER BY RAND()
        """

    # User wanted only 1 or 5 results
    if entry_choice != 0:
        lim_string = str(entry_choice)
        query += "LIMIT "
        query += lim_string
        results = db_ops.query_all_values(query)
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
        WHERE songLength < 150 AND deleted = 0
        ORDER BY RAND()
        """
    else:
        query = """
        SELECT songName
        FROM Songs
        WHERE songLength > 150 AND deleted = 0
        ORDER BY RAND()
        """
    # User wanted only 1 or 5 results
    if entry_choice != 0:
        lim_string = str(entry_choice)
        query += "LIMIT "
        query += lim_string
        results = db_ops.query_all_values(query)
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
        WHERE Movies.name = "%s" AND Reviews.deleted = 0
        ORDER BY RAND()
        """
        # dictionary = {"selection": choices[name_index]}
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
        results = db_ops.query_all_values(query % choices[name_index])
        helper.pretty_print(results)

    else:
        if filter_choice == 2:
            query = """
            SELECT Movies.name, Reviews.username, Reviews.text
            FROM Reviews
            INNER JOIN Movies ON Movies.movieID = Reviews.movieID
            WHERE Reviews.score > 7.5 AND Reviews.deleted = 0
            ORDER BY RAND()
            """
        else:
            query = """
            SELECT Movies.name, Reviews.username, Reviews.text
            FROM Reviews
            INNER JOIN Movies ON Movies.movieID = Reviews.movieID
            WHERE Reviews.score < 7.5 AND Reviews.deleted = 0
            ORDER BY RAND()
            """
        # User wanted only 1 or 5 results
        if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
            results = db_ops.query_all_values(query)
            helper.pretty_print(results)
        else:
            results = db_ops.query_all_values(query)
            helper.pretty_print(results)

# HAS NOT BEEN TESTED
# Picks a random movie for the user to watch
def randomMoviePicker():
    query = """
    SELECT name, runtime, genre
    FROM Movies
    ORDER BY RAND()
    LIMIT 1
    """

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
# Actors(ActorID, Name, Age, NominatedForAward, Hotness, Date)
#Bro there is no way we have a hotness attribute
def addActor():
#def addActor(actorID, name, age, nominatedForAward, hotness, date, movieBeenIn):
    # This takes the actor's info, adds an entry, then prompts to ask
    # if the actor has been in a movie. If yes, get the name, check with
    # the database, and if that movie exists, make an entry in the
    # MovieActor table


    #----------------------------NOT TESTED----------------------------w
    # query = '''
    # INSERT INTO Actors VALUES(\'''' + name + '''\',\'''' + age + '''\',\'''' + nominatedForAward + '''\',\'''' + hotness + '''\',\'''' + date + '''\')'''
    # db_operations.insert_single_record(query)

    # #if actor has been in a movie
    # if(movieBeenIn != "NA"):
    #     #check if movie exists
    #     query = '''
    #     SELECT name
    #     FROM Movies
    #     WHERE name = \'''' + movieBeenIn + '''\''''
    #     movieList = db_operations.single_attribute(query)
    #     if(movieList[0] == movieBeenIn):
    #         #add to MovieActors
    #         query = '''
    #         INSERT INTO MovieActors VALUES(\'''' + actorID + '''\',\'''' + movieBeenIn + '''\', 1)'''
    #         db_operations.insert_single_record(query)
    #     else:
    #         print("Movie does not exist in database")
    #------------------------------------------------------------------
    pass

# HAS NOT BEEN TESTED
# Allows a user to add a song to the database
# Songs(SongID, ComposerID*, MovieID*, ConnorsIncrediblyProfessionalAndPurelyObjectiveRating, SongLength)
def addSong():
#def addSong(songID, composerID, movieID, connorsIncrediblyProfessionalAndPurelyObjectiveRating, songLength):
    # Get the song's title, then composer. If composer doesn't exist yet,
    # get that info first. Then continue with song's info

    #----------------------------------------NOT TESTED------------------------------------------------------
    # #what do we do if composerID doesn't exist yet?
    # checkComposerQuery = '''
    #     SELECT ComposerID
    #     FROM Composers
    # '''
    
    # query = '''
    #     INSERT INTO Songs VALUES(\'''' + songID + '''\',\'''' + composerID + '''\',\'''' + movieID + '''\',\'''' + connorsIncrediblyProfessionalAndPurelyObjectiveRating + '''\',\'''' + songLength + '''\')
    # '''
    # db_operations.insert_single_record(query)
    #----------------------------------------------------------------------------------------------

    pass

# HAS NOT BEEN TESTED
# Allows a user to add a review for an existing movie
#Reviews(ReviewID, Username, MovieID*, Score, Text)
def addReview():
# def addReview(reviewID, username, movieID, score, text):
#     # Check if movie exists, then add review
    
#     checkQuery = '''
#     SELECT *
#     FROM Movies
#     WHERE MovieID = \'''' + movieID + '''\''''
#     results = db_ops.whole_record(checkQuery)
#     if (results):
#         query = '''
#         INSERT INTO Reviews VALUES(\'''' + reviewID + '''\',\'''' + username + '''\',\'''' + movieID + '''\',\'''' + score + '''\',\'''' + text + '''\')
#         '''
#         db_ops.insert_single_record(query)
#     else:
#         print("Movie does not exist in database")
    pass

# Special Filtering Options Menu (Basically all of the special/complex queries)
def special_filtering_menu():
    print(
        """You have the following options for accessing special table filters:
        1 - Find Actors by Movie
        2 - Display number of Actors in each Movie
        3 - Find Directors who have directed movies with a gross profit over 300 million
        4 - Find Directors who have directed movies with a gross profit under 300 million
        5 - Find Directors by Studio
        """
    )
    table_choice = helper.get_choice([1, 2, 3, 4, 5, 6])

    # Optional limit to how many entries user views
    print("How many entries would you like returned?")
    print("Enter 1, 5, or 0 for all entries")
    number = helper.get_choice([1, 5, 0])

    if table_choice == 1:
        actors_by_movie(number)
    if table_choice == 2:
        actors_per_movie(number)
    if table_choice == 3:
        directors_high_grossing(number)
    if table_choice == 4:
        directors_low_grossing(number)
    if table_choice == 5:
        directors_by_studio(number)

# Query that asks user for a movie, and based on the movie, obtains those actors from a triple join query
def actors_by_movie(entry_choice):
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
    movie_name = choices[name_index]

    query = """
    SELECT Actors.name
    FROM MovieActors
    INNER JOIN Actors ON Actors.actorID = MovieActors.actorID
    INNER JOIN Movies ON Movies.movieID = MovieActors.movieID
    WHERE Movies.name = "%s"
    ORDER BY RAND()
    """

    if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
    results = db_ops.query_all_values(query % movie_name)
    helper.pretty_print(results)

# Query that provides the user the number of actors per movie using a Group By / Aggregate Clause
def actors_per_movie(entry_choice):
    query = """
    SELECT Movies.name AS movieName, COUNT(DISTINCT MovieActors.actorID) AS actorCount
    FROM Movies
    INNER JOIN MovieActors ON MovieActors.movieID = Movies.movieID
    GROUP BY movieName
    ORDER BY RAND()
    """

    if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
    results = db_ops.query_all_values(query)
    helper.pretty_print(results)

# Query that provides the user the names of Directors whose movies have had a gross profit over 300 million using a subquery
def directors_high_grossing(entry_choice):
    query = """
    SELECT Directors.name
    FROM Directors
    INNER JOIN (
        SELECT Movies.directorID
        FROM Movies
        WHERE grossProfit > 300000000
    ) AS HighGrossingMovie
    ON HighGrossingMovie.directorID = Directors.directorID
    ORDER BY RAND()
    """

    if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
    results = db_ops.query_all_values(query)
    helper.pretty_print(results)

# Query that provides the user the names of Directors whose movies have had a gross profit over 300 million using a subquery
def directors_low_grossing(entry_choice):
    query = """
    SELECT Directors.name
    FROM Directors
    INNER JOIN (
        SELECT Movies.directorID
        FROM Movies
        WHERE grossProfit < 300000000
    ) AS HighGrossingMovie
    ON HighGrossingMovie.directorID = Directors.directorID
    ORDER BY RAND()
    """

    if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
    results = db_ops.query_all_values(query)
    helper.pretty_print(results)

# Query that asks the user for a studio, and based on that studio, obtains the director(s) who have worked with the studio using a triple join
def directors_by_studio(entry_choice):
    name_query = """
    SELECT DISTINCT name
    FROM Studios;
    """
    # Show user movie names in database, then get their input
    print("Names from Studio database: ")
    names = db_ops.single_attribute(name_query)

    choices = {}
    for i in range(len(names)):
        print(i, names[i])
        choices[i] = names[i]
    name_index = helper.get_choice(choices.keys())
    studio_name = choices[name_index]

    query = """
    SELECT Directors.name
    FROM Movies
    INNER JOIN Directors ON Directors.directorID = Movies.directorID
    INNER JOIN Studios ON Studios.studioID = Movies.studioID
    WHERE Studios.name = "%s"
    ORDER BY RAND()
    """

    if entry_choice != 0:
            lim_string = str(entry_choice)
            query += "LIMIT "
            query += lim_string
    results = db_ops.query_all_values(query % studio_name)
    helper.pretty_print(results)

# MAIN CODE:
try:
    populate_with_sample_data()
except:
    print("Data in table already exists. Proceeding as usual...")

while (True):
    print('''Currently, you have the following options:
    1 - Print out tables
    2 - Filter tables
    3 - Pick a random movie
    4 - Even more special table filtering
    0 - Quit
    ''')
    menu_choice = helper.get_choice([0,1,2,3,4])
    if menu_choice == 1:
        print_menu()
        continue
    if menu_choice == 2:
        filter_menu()
        continue
    if menu_choice == 3:
        randomMoviePicker()
    if menu_choice == 4:
        special_filtering_menu()
    if menu_choice == 0:
        break
db_ops.destructor()
