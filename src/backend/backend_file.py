from helper import helper
from db_operations import db_operations
import pandas as pd
import mysql.connector

# python backend_file.py

# Creating the schema on locally prior to opening the MovieBot schema via db_operations
first_conn = mysql.connector.connect(host="localhost",
    user="root",
    password="cpsc408",
    auth_plugin='mysql_native_password')

first_cur = first_conn.cursor()
first_cur.execute("CREATE SCHEMA IF NOT EXISTS MovieBot;")
first_conn.close()

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

    
    movies_view_query = """
    CREATE VIEW generalizedMoviesView AS
        SELECT name, runtime, budget, grossProfit, genre, year, pSafeRating
        FROM movies
        ORDER BY RAND();
    """
    db_ops.generalized_execute(movies_view_query)
    
    actors_view_query = """
    CREATE VIEW generalizedActorsView AS
        SELECT name, age, hotness
        FROM actors
        ORDER BY RAND();
    """
    db_ops.generalized_execute(actors_view_query)

    composers_view_query = """
    CREATE VIEW generalizedComposersView AS
        SELECT name, age
        FROM composers
        ORDER BY RAND();
    """
    db_ops.generalized_execute(composers_view_query)

    directors_view_query = """
    CREATE VIEW generalizedDirectorsView AS
        SELECT name, age
        FROM composers
        ORDER BY RAND();
    """
    db_ops.generalized_execute(directors_view_query)

    songs_view_query = """
    CREATE VIEW generalizedSongsView AS
        SELECT songName, songLength, ConnorsIncrediblyProfessionalAndPurelyObjectiveRating
        FROM songs
        WHERE deleted = 0
        ORDER BY RAND();
    """
    db_ops.generalized_execute(songs_view_query)

    studios_view_query = """
    CREATE VIEW generalizedStudiosView AS
        SELECT name, location
        FROM studios
        ORDER BY RAND();
    """
    db_ops.generalized_execute(studios_view_query)

    reviews_view_query = """
    CREATE VIEW generalizedReviewsView AS
        SELECT Reviews.username, Movies.name, Reviews.score, Reviews.text
        FROM Reviews
        INNER JOIN Movies ON Movies.movieID = Reviews.movieID
        WHERE deleted = 0
        ORDER BY RAND();
    """
    db_ops.generalized_execute(songs_view_query)
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

# Allows a user to add a song to the database
# Songs(SongID, ComposerID*, MovieID*, ConnorsIncrediblyProfessionalAndPurelyObjectiveRating, SongLength)
def addSong():
    # get names of movies
    movie_query = """
    SELECT DISTINCT name
    FROM Movies;
    """
    # Show user genres in database, then get their input
    print("Movie Titles from Movie database: ")
    movie_names = db_ops.single_attribute(movie_query)

    movie_choices = {}
    for i in range(len(movie_names)):
        print(i, movie_names[i])
        movie_choices[i] = movie_names[i]
    movie_index = helper.get_choice(movie_choices.keys())

    movie_id_query  = """
    SELECT DISTINCT movieID
    FROM Movies
    WHERE name = "%s"
    """
    movie_result = db_ops.single_record(movie_id_query % movie_names[movie_index])

    # get names of composers
    composer_query = """
    SELECT DISTINCT name
    FROM Composers;
    """
    # Show user genres in database, then get their input
    print("Composer names from Composer database: ")
    composer_names = db_ops.single_attribute(composer_query)

    composer_choices = {}
    for i in range(len(composer_names)):
        print(i, composer_names[i])
        composer_choices[i] = composer_names[i]
    composer_index = helper.get_choice(composer_choices.keys())

    composer_id_query  = """
    SELECT DISTINCT composerID
    FROM Composers
    WHERE name = "%s"
    """
    composer_result = db_ops.single_record(composer_id_query % composer_names[composer_index])

    songname_set = False
    while (songname_set == False):
        song_name = input("Please enter the name of the song that you want to add. It must be at least 3 characters and do not include spaces: ")
        if len(song_name) > 2:
            songname_set = True
            break
        else:
            print("Username must be at least 3 characters. Please try again")
            continue

    duration_set = False
    while (duration_set == False):
        duration = input("Please enter the duration of the song in minutes. This must be an integer greater than 0: ")
        if duration.isdigit() == True:
            if int(duration) > 0:
                song_length = int(duration)
                duration_set = True
                break
            else:
                print("Song duration must be longer than 0 minutes")
                continue
        else:
            print("Invalid input. Enter an integer greater than 0.")
            continue
        
    insert_query = """
    START TRANSACTION;
    INSERT INTO Songs (songName, composerID, movieID, songLength, ConnorsIncrediblyProfessionalAndPurelyObjectiveRating, deleted)
    VALUES ("%s", %d, %d, %d, "placeholder", 0);
    INSERT INTO songs_log VALUES (USER(), 'Insert', 'Inserted song with name: "%s"');
    COMMIT;
    """
    db_ops.generalized_execute(insert_query % (song_name, composer_result, movie_result, song_length, song_name))

def updateSongDuration():
    id_set = False
    while (id_set == False):
        id_input = input("Please enter the ID of the song you would like to edit. This must be an integer greater than 0: ")
        if id_input.isdigit() == True:
            if int(id_input) > 0:
                search_id = int(id_input)
                search_query = """
                SELECT COUNT(DISTINCT songID)
                FROM Songs
                WHERE songID = %d AND deleted = 0;
                """
                search_result = db_ops.single_record(search_query % search_id)
                # Id does not exist or Id belongs to a deleted Song
                if search_result == 0:
                    print("Song does not exist or has been deleted. please try again.")
                    continue
                # Id exists within database
                else:
                    print("Id found...")
                    id_set = True
                    song_ID = search_id
                    break
            else:
                print("Song ID must be greater than 0.")
                continue
        else:
            print("Invalid input. Enter an integer greater than 0.")
            continue
    
    duration_set = False
    while (duration_set == False):
        duration = input("Please enter the new duration of the song in minutes. This must be an integer greater than 0: ")
        if duration.isdigit() == True:
            if int(duration) > 0:
                song_length = int(duration)
                duration_set = True
                break
            else:
                print("Song's new duration must be longer than 0 minutes")
                continue
        else:
            print("Invalid input. Enter an integer greater than 0.")
            continue

    # obtain old song duration for log table
    log_duration = """
    SELECT songLength
    FROM SONGS
    WHERE songID = %d
    """
    old_duration = db_ops.single_record(log_duration % song_ID)

    # Transaction to update Song Duration and Logs old value
    update_query = """
    START TRANSACTION;
    UPDATE Songs
    SET
        songLength = %d
    WHERE songID = %d;
    INSERT INTO songs_log VALUES (USER(), "Update","Updates songID %d's length from %d to %d");
    COMMIT;
    """
    db_ops.generalized_execute(update_query % (song_length, song_ID, song_ID, old_duration, song_length))

# Allows a user to add a review for an existing movie
#Reviews(ReviewID, Username, MovieID*, Score, Text)
def addReview():
    # get names of movies
    movie_query = """
    SELECT DISTINCT name
    FROM Movies;
    """
    # Show user genres in database, then get their input
    print("Movie Titles from Movie database: ")
    movie_names = db_ops.single_attribute(movie_query)

    choices = {}
    for i in range(len(movie_names)):
        print(i, movie_names[i])
        choices[i] = movie_names[i]
    index = helper.get_choice(choices.keys())

    movie_id_query  = """
    SELECT DISTINCT movieID
    FROM Movies
    WHERE name = "%s"
    """
    movie_result = db_ops.single_record(movie_id_query % movie_names[index])

    username_set = False
    while (username_set == False):
        username = input("Please enter the username you want associated with the review. Do not include spaces: ")
        if len(username) > 2:
            username_set = True
            break
        else:
            print("Username must be at least 3 characters. Please try again")
            continue
    print("Please enter your score for the movie. This must be an integer from 1 to 10.")
    score = helper.get_choice([1,2,3,4,5,6,7,8,9,10])

    text_set = False
    while (text_set == False):
        text = input("Please enter your review of the movie. This must be at least 3 characters and less than 300 characters. Use underscores in place of spaces: ")
        if len(text) > 2 and len(text) < 300:
            text_set = True
            break
        else:
            print("Review Text must be at least 3 characters and less than 300 characters. Please try again")
            continue

    insert_query = """
    START TRANSACTION;
    INSERT INTO Reviews (username, movieID, score, text, deleted)
    VALUES ("%s", %d, %d, "%s", 0);
    INSERT INTO reviews_log VALUES (USER(), 'Insert', 'Inserted review with username: "%s"');
    COMMIT;
    """
    db_ops.generalized_execute(insert_query % (username, movie_result, score, text, username))

def updateReviewText():
    # Obtain reviewID from user
    id_set = False
    while (id_set == False):
        id_input = input("Please enter the ID of the review you would like to edit. This must be an integer greater than 0: ")
        if id_input.isdigit() == True:
            if int(id_input) > 0:
                search_id = int(id_input)
                search_query = """
                SELECT COUNT(DISTINCT reviewID)
                FROM Reviews
                WHERE reviewID = %d AND deleted = 0;
                """
                search_result = db_ops.single_record(search_query % search_id)
                # Id does not exist or Id belongs to a deleted Review
                if search_result == 0:
                    print("Review does not exist or has been deleted. please try again.")
                    continue
                # Id exists within database
                else:
                    print("Id found...")
                    id_set = True
                    review_id = search_id
                    break
            else:
                print("Review ID must be greater than 0.")
                continue
        else:
            print("Invalid input. Enter an integer greater than 0.")
            continue
    
    text_set = False
    while (text_set == False):
        text = input("Please enter the new review of the movie. This must be at least 3 characters and less than 300 characters. Use underscores in place of spaces: ")
        if len(text) > 2 and len(text) < 300:
            text_set = True
            break
        else:
            print("New Review Text must be at least 3 characters and less than 300 characters. Please try again")
            continue

    update_query = """
    START TRANSACTION;
    UPDATE Reviews
    SET text = "%s"
    WHERE reviewID = %d;
    INSERT INTO reviews_log VALUES (USER(), "UPDATE", "Updated reviewID %d's text to: %s");
    COMMIT;
    """
    db_ops.generalized_execute(update_query % (text, review_id, review_id, text))


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

def view_menu():
    print(
    """Which table would you like a general view of?
    1 - Movies
    2 - Actors
    3 - Directors
    4 - Composers
    5 - Songs
    6 - Studios
    7 - Reviews
    """
    )
    table_choice = helper.get_choice([1, 2, 3, 4, 5, 6, 7])

    if table_choice == 1:
        query = """
        SELECT *
        FROM generalizedMoviesView;
        """
    if table_choice == 2:
        query = """
        SELECT *
        FROM generalizedActorsView;
        """
    if table_choice == 3:
        query = """
        SELECT *
        FROM generalizedDirectorsView;
        """
    if table_choice == 4:
        query = """
        SELECT *
        FROM generalizedComposersView;
        """
    if table_choice == 5:
        query = """
        SELECT *
        FROM generalizedSongsView;
        """
    if table_choice == 6:
        query = """
        SELECT *
        FROM generalizedStudiosView;
        """
    if table_choice == 7:
        query = """
        SELECT *
        FROM generalizedReviewsView;
        """
    results = db_ops.query_all_values(query)
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
    5 - Print out generalized view of table 
    6 - Add a Song
    7 - Update a Song's Duration
    8 - Insert a Review
    9 - Update a Review's Text
    0 - Quit
    ''')
    menu_choice = helper.get_choice([0,1,2,3,4,5,6,7,8,9])
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
    if menu_choice == 5:
        view_menu()
    if menu_choice == 6:
        addSong()
    if menu_choice == 7:
        updateSongDuration()
    if menu_choice == 8:
        addReview()
    if menu_choice == 9:
        updateReviewText()
    if menu_choice == 0:
        break
db_ops.destructor()
