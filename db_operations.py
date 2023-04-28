import mysql.connector

class db_operations():

    # constructor with connection back to database
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost", 
                               user="root",
                               password="cpsc408",
                               auth_plugin='mysqlnative_password',
                               database="MovieBot"
                               )
        self.cursor = self.conn.cursor()
        print("Connection made...")

        self.cursor.execute("CREATE SCHEMA IF NOT EXISTS MovieBot;")

    #destructor that close connection to database
    def destructor(self):
        self.connection.close()
        print("connection closed...")

    def create_database_tables(self):
        # Creates movies table with movieID as Primary Key
        query = '''
        CREATE TABLE Movies(
            movieID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            runtime INT,
            budget INT,
            grossProfit INT,
            criticScore INT,
            viewerScore INT,
            genre VARCHAR(25),
            year INT,
            nominatedForAward BOOLEAN DEFAULT false,
            pSafeRating VARCHAR(50),
            CONSTRAINT CHK_Movie CHECK (runtime > 0 AND budget > 0 AND year >= 1895 AND year < 3000)
        );
        '''
        self.cursor.execute(query)

        # Creates actors table with actorID as Primary Key
        query2 = '''
        CREATE TABLE Actors(
            actorID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            age INT,
            hotness INT,
            date VARCHAR(25),
            CONSTRAINT CHK_Actor CHECK (age > 0)
        );
        '''
        self.cursor.execute(query2)

        # Creates MovieActor table with actorID and movieID as the composite Primary key
        query3 = '''
        CREATE TABLE MovieActors(
            PRIMARY KEY (actorID, movieID) INT NOT NULL,
            wasLead BOOLEAN
        );
        '''
        self.cursor.execute(query3)

        # Creates Directors table with directorID
        query4 = '''
        CREATE TABLE Directors(
            directorID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(30) NOT NULL,
            age INT,
            CONSTRAINT CHK_Director CHECK (age > 0)
        );
        '''
        self.cursor.execute(query4)

        # Creates Composers table with composerID as the Primary key
        query5 = '''
        CREATE TABLE Composers(
            composerID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(30) NOT NULL,
            age INT,
            movieCount INT,
            CONSTRAINT CHK_Composer CHECK (age > 0)
        );
        '''
        self.cursor.execute(query5)

        # Creates Songs table with songID as the Primary key
        query6 = '''
        CREATE TABLE Songs(
            songID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            songName VARCHAR(50) NOT NULL,
            FOREIGN KEY (composerID) REFERENCES Composers(composerID),
            FOREIGN KEY (movieID) REFERENCES Movies(movieID),
            songLength INT,
            ConnorsIncrediblyProfessionalAndPurelyObjectiveRating VARCHAR(30),
            CONSTRAINT CHK_Song CHECK (songLength > 0)
        );
        '''
        self.cursor.execute(query6)

        # Creates Studios table with studioID as the Primary key
        query7 = '''
        CREATE TABLE Songs(
            studioID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            location VARCHAR(50)
        );
        '''
        self.cursor.execute(query7)

        # Creates Reviews table with reviewID as the Primary key
        query8 = '''
        CREATE TABLE Reviews(
            reviewID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) NOT NULL,
            FOREIGN KEY (movieID) REFERENCES Movies(movieID),
            score INT NOT NULL,
            text VARCHAR(300),
            CONSTRAINT CHK_Score CHECK (score >= 0 AND score <= 11)
        );
        '''
        self.cursor.execute(query8)

        print("Tables Created!")

   #we want cursor to run query and return value of the cell when I run it
    def single_record(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchone() [0] #fetchone() returns first row of query, [0] returns first cell of that row
        #can give us just the value of the COUNT(*)

    #we want cursor to run query and return value of the cell when I run it
    def whole_record(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_single_record(self,query):
        self.cursor.execute(query)
        self.connection.commit()

    #function to bulk insert records
    #runs query for each record in "records"
    def bulk_insert(self,query,records):
        self.cursor.executemany(query,records)
        self.connection.commit()
        print("query bulk executed...")

    #function that returns values of a single attribute
    def single_attribute(self,query):
        self.cursor.execute(query)  #results of query in the cursor
        results = self.cursor.fetchall() #fetchall() returns all rows of query in a 2d array with a bunch of arrays of length 1
        results = [i[0] for i in results]   #for everything in results make it equal to the first cell of that row and add it to results
        if("None" in results):
            results.remove("None")    #remove None values
        return results

    def name_placeholder_query(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall() #fetchall() returns all rows of query in a 2d array with a bunch of arrays of length 1
        results = [i[0] for i in results]   #for everything in results make it equal to the first cell of that row and add it to results
        return results
    
    def name_placeholder_query2(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall()
        return results
    
    def update_record(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()
        print("update query executed...")

    def update_record2(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        print("update query executed...")

    #uses a named placeholder query to return all values in each row
    def name_placeholder_query_all_values(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall()
        return results

    def delete_record(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()
        print("delete query executed...")