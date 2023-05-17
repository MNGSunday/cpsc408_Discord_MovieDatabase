-- MySQL dump 10.13  Distrib 8.0.32, for macos12.6 (arm64)
--
-- Host: localhost    Database: moviebot
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actors`
--

DROP TABLE IF EXISTS `actors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actors` (
  `actorID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `age` int DEFAULT NULL,
  `hotness` int DEFAULT NULL,
  `date` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`actorID`),
  CONSTRAINT `CHK_Actor` CHECK ((`age` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actors`
--

LOCK TABLES `actors` WRITE;
/*!40000 ALTER TABLE `actors` DISABLE KEYS */;
INSERT INTO `actors` VALUES (1,'Owen Wilson',54,99999999,'For Sure'),(2,'Larry the Cable Guy',60,8,'Who Wouldn\'t??'),(3,'Brad Pitt',59,7,'He\'s Rich I guess'),(4,'Jerry Seinfeld',68,2,'He a Bee'),(5,'Alden Ehrenreich',33,5,'Eh'),(6,'Miles Teller',36,3,'Too Goofy'),(7,'J.K. Simmons',68,1,'Too Old');
/*!40000 ALTER TABLE `actors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `actors_log`
--

DROP TABLE IF EXISTS `actors_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actors_log` (
  `user` varchar(50) DEFAULT NULL,
  `action` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actors_log`
--

LOCK TABLES `actors_log` WRITE;
/*!40000 ALTER TABLE `actors_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `actors_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `composers`
--

DROP TABLE IF EXISTS `composers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `composers` (
  `composerID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `age` int DEFAULT NULL,
  `movieCount` int DEFAULT NULL,
  PRIMARY KEY (`composerID`),
  CONSTRAINT `CHK_Composer` CHECK ((`age` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `composers`
--

LOCK TABLES `composers` WRITE;
/*!40000 ALTER TABLE `composers` DISABLE KEYS */;
INSERT INTO `composers` VALUES (1,'Michael Giacchino',55,67),(2,'Rupert Gregson-Williams',56,46),(3,'John Williams',91,125),(4,'John Powell',59,79),(5,'Justin Hurtwitz',38,6);
/*!40000 ALTER TABLE `composers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `composers_log`
--

DROP TABLE IF EXISTS `composers_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `composers_log` (
  `user` varchar(50) DEFAULT NULL,
  `action` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `composers_log`
--

LOCK TABLES `composers_log` WRITE;
/*!40000 ALTER TABLE `composers_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `composers_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `directors`
--

DROP TABLE IF EXISTS `directors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `directors` (
  `directorID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `age` int DEFAULT NULL,
  PRIMARY KEY (`directorID`),
  CONSTRAINT `CHK_Director` CHECK ((`age` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `directors`
--

LOCK TABLES `directors` WRITE;
/*!40000 ALTER TABLE `directors` DISABLE KEYS */;
INSERT INTO `directors` VALUES (1,'John Lasseter',66),(2,'Quentin Tarantino',60),(3,'Simon J. Smith',54),(4,'Ron Howard',69),(5,'Damien Chazelle',38);
/*!40000 ALTER TABLE `directors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `directors_log`
--

DROP TABLE IF EXISTS `directors_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `directors_log` (
  `user` varchar(50) DEFAULT NULL,
  `action` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `directors_log`
--

LOCK TABLES `directors_log` WRITE;
/*!40000 ALTER TABLE `directors_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `directors_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `generalizedactorsview`
--

DROP TABLE IF EXISTS `generalizedactorsview`;
/*!50001 DROP VIEW IF EXISTS `generalizedactorsview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `generalizedactorsview` AS SELECT 
 1 AS `songName`,
 1 AS `songLength`,
 1 AS `ConnorsIncrediblyProfessionalAndPurelyObjectiveRating`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `generalizedcomposersview`
--

DROP TABLE IF EXISTS `generalizedcomposersview`;
/*!50001 DROP VIEW IF EXISTS `generalizedcomposersview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `generalizedcomposersview` AS SELECT 
 1 AS `name`,
 1 AS `age`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `generalizeddirectorsview`
--

DROP TABLE IF EXISTS `generalizeddirectorsview`;
/*!50001 DROP VIEW IF EXISTS `generalizeddirectorsview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `generalizeddirectorsview` AS SELECT 
 1 AS `name`,
 1 AS `age`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `generalizedmoviesview`
--

DROP TABLE IF EXISTS `generalizedmoviesview`;
/*!50001 DROP VIEW IF EXISTS `generalizedmoviesview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `generalizedmoviesview` AS SELECT 
 1 AS `name`,
 1 AS `runtime`,
 1 AS `budget`,
 1 AS `grossProfit`,
 1 AS `genre`,
 1 AS `year`,
 1 AS `pSafeRating`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `generalizedreviewsview`
--

DROP TABLE IF EXISTS `generalizedreviewsview`;
/*!50001 DROP VIEW IF EXISTS `generalizedreviewsview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `generalizedreviewsview` AS SELECT 
 1 AS `username`,
 1 AS `name`,
 1 AS `score`,
 1 AS `text`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `generalizedsongsview`
--

DROP TABLE IF EXISTS `generalizedsongsview`;
/*!50001 DROP VIEW IF EXISTS `generalizedsongsview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `generalizedsongsview` AS SELECT 
 1 AS `songName`,
 1 AS `songLength`,
 1 AS `ConnorsIncrediblyProfessionalAndPurelyObjectiveRating`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `generalizedstudiosview`
--

DROP TABLE IF EXISTS `generalizedstudiosview`;
/*!50001 DROP VIEW IF EXISTS `generalizedstudiosview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `generalizedstudiosview` AS SELECT 
 1 AS `name`,
 1 AS `location`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `movieactors`
--

DROP TABLE IF EXISTS `movieactors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movieactors` (
  `actorID` int NOT NULL,
  `movieID` int NOT NULL,
  `wasLead` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`actorID`,`movieID`),
  KEY `movieID` (`movieID`),
  CONSTRAINT `movieactors_ibfk_1` FOREIGN KEY (`actorID`) REFERENCES `actors` (`actorID`),
  CONSTRAINT `movieactors_ibfk_2` FOREIGN KEY (`movieID`) REFERENCES `movies` (`movieID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movieactors`
--

LOCK TABLES `movieactors` WRITE;
/*!40000 ALTER TABLE `movieactors` DISABLE KEYS */;
INSERT INTO `movieactors` VALUES (1,1,1),(2,1,1),(3,2,1),(4,3,1),(5,4,1),(6,5,1),(7,5,1);
/*!40000 ALTER TABLE `movieactors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movieactors_log`
--

DROP TABLE IF EXISTS `movieactors_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movieactors_log` (
  `user` varchar(50) DEFAULT NULL,
  `action` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movieactors_log`
--

LOCK TABLES `movieactors_log` WRITE;
/*!40000 ALTER TABLE `movieactors_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `movieactors_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movies`
--

DROP TABLE IF EXISTS `movies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movies` (
  `movieID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `directorID` int NOT NULL,
  `composerID` int NOT NULL,
  `studioID` int NOT NULL,
  `runtime` int DEFAULT NULL,
  `budget` int DEFAULT NULL,
  `grossProfit` int DEFAULT NULL,
  `criticScore` int DEFAULT NULL,
  `viewerScore` int DEFAULT NULL,
  `genre` varchar(25) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `nominatedForAward` tinyint(1) DEFAULT '0',
  `pSafeRating` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`movieID`),
  KEY `directorID` (`directorID`),
  KEY `composerID` (`composerID`),
  KEY `studioID` (`studioID`),
  CONSTRAINT `movies_ibfk_1` FOREIGN KEY (`directorID`) REFERENCES `directors` (`directorID`),
  CONSTRAINT `movies_ibfk_2` FOREIGN KEY (`composerID`) REFERENCES `composers` (`composerID`),
  CONSTRAINT `movies_ibfk_3` FOREIGN KEY (`studioID`) REFERENCES `studios` (`studioID`),
  CONSTRAINT `CHK_Movie` CHECK (((`runtime` > 0) and (`budget` > 0) and (`year` >= 1895) and (`year` < 3000)))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movies`
--

LOCK TABLES `movies` WRITE;
/*!40000 ALTER TABLE `movies` DISABLE KEYS */;
INSERT INTO `movies` VALUES (1,'Cars 2',1,1,1,106,200000000,599000000,40,49,'War/Comedy',2011,1,'Borderline Banned'),(2,'Inglourious Basterds',2,2,2,153,70000000,321400000,89,88,'War/Comedy',2009,1,'NOTSAFE NOTSAFE NOTSAFE'),(3,'Bee Movie',3,3,3,91,150000000,293500000,49,53,'Kids & Family',2007,0,'Bzzzzz'),(4,'Solo: A Star Wars Story',4,4,4,135,275000000,393200000,69,63,'Sci-Fi/Adventure',2018,1,'Rebel Scum'),(5,'Whiplash',5,5,5,107,3300000,49000000,94,94,'Drama/Music',2014,1,'*Angry Drum Sounds*');
/*!40000 ALTER TABLE `movies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movies_log`
--

DROP TABLE IF EXISTS `movies_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movies_log` (
  `user` varchar(50) DEFAULT NULL,
  `action` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movies_log`
--

LOCK TABLES `movies_log` WRITE;
/*!40000 ALTER TABLE `movies_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `movies_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `movies_with_director_composer_studio`
--

DROP TABLE IF EXISTS `movies_with_director_composer_studio`;
/*!50001 DROP VIEW IF EXISTS `movies_with_director_composer_studio`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `movies_with_director_composer_studio` AS SELECT 
 1 AS `movieID`,
 1 AS `movieName`,
 1 AS `directorID`,
 1 AS `composerID`,
 1 AS `studioID`,
 1 AS `runtime`,
 1 AS `budget`,
 1 AS `grossProfit`,
 1 AS `criticScore`,
 1 AS `viewerScore`,
 1 AS `genre`,
 1 AS `year`,
 1 AS `nominatedForAward`,
 1 AS `pSafeRating`,
 1 AS `directorName`,
 1 AS `directorAge`,
 1 AS `composerName`,
 1 AS `composerAge`,
 1 AS `composerMovieCount`,
 1 AS `studioName`,
 1 AS `studioLocation`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `reviewID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `movieID` int NOT NULL,
  `score` int NOT NULL,
  `text` varchar(300) DEFAULT NULL,
  `deleted` int NOT NULL,
  PRIMARY KEY (`reviewID`),
  KEY `movieID` (`movieID`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`movieID`) REFERENCES `movies` (`movieID`),
  CONSTRAINT `CHK_Score` CHECK (((`score` >= 0) and (`score` <= 11)))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,'condog7',1,10,'Truly the greatest movie of our generation',1),(2,'condog7',2,5,'aowiefjaoweifj',0),(3,'condog7',3,8,'Bzzz... Bzz!? Bzz bzz bzz bzzzzz bzzzzzzz bz bzbzzz bz!!',0),(4,'condog7',4,9,'I never thought a slave robot revolution in Star Wars would be the highlight of a movie yet here we are',0),(5,'condog7',5,5,'I haven\'t seen this movie before',0),(6,'puttputt',1,10,'I bet Barry the Bee could save the Zoo, too!',0),(7,'puttputt',4,8,'Hey, I went to space once!',0),(8,'puttputt',3,7,'Bees?!',0),(11,'Nugget',5,7,'I_didn\'t_watch_it',1),(12,'test uesrname',1,5,'test review',0),(13,'test uesrname',1,5,'test review',0),(14,'christofuy',1,10,'aowiefjaoweifjaoweifjawefawefawefawefawefawef',1),(15,'christofuy',1,10,'oij',0);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_log`
--

DROP TABLE IF EXISTS `reviews_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews_log` (
  `user` varchar(50) DEFAULT NULL,
  `action_type` varchar(10) NOT NULL,
  `action` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_log`
--

LOCK TABLES `reviews_log` WRITE;
/*!40000 ALTER TABLE `reviews_log` DISABLE KEYS */;
INSERT INTO `reviews_log` VALUES ('root@localhost','UPDATE','Updated reviewID 8\'s text to: Beeeeeeeees'),('root@localhost','UPDATE','Updated reviewID 8\'s text to: Bees?!'),('root@localhost','Insert','Inserted review with username: \"Nugget\"'),('root@localhost','Delete','Soft deleted review with ID: 11'),('christofuy','Delete','Deleted review with id: 0'),('christofuy','Delete','Deleted review with id: 14'),('christofuy','Insert','Inserted review with id: 15'),('christofuy','Delete','Deleted review with id: 1'),('christofuy','Update','Updated review with id: 0'),('christofuy','Update','Updated review with id: 0');
/*!40000 ALTER TABLE `reviews_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `songs`
--

DROP TABLE IF EXISTS `songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `songs` (
  `songID` int NOT NULL AUTO_INCREMENT,
  `songName` varchar(50) NOT NULL,
  `composerID` int NOT NULL,
  `movieID` int NOT NULL,
  `songLength` int DEFAULT NULL,
  `ConnorsIncrediblyProfessionalAndPurelyObjectiveRating` varchar(30) DEFAULT NULL,
  `deleted` int NOT NULL,
  PRIMARY KEY (`songID`),
  KEY `composerID` (`composerID`),
  KEY `movieID` (`movieID`),
  CONSTRAINT `songs_ibfk_1` FOREIGN KEY (`composerID`) REFERENCES `composers` (`composerID`),
  CONSTRAINT `songs_ibfk_2` FOREIGN KEY (`movieID`) REFERENCES `movies` (`movieID`),
  CONSTRAINT `CHK_Song` CHECK ((`songLength` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `songs`
--

LOCK TABLES `songs` WRITE;
/*!40000 ALTER TABLE `songs` DISABLE KEYS */;
INSERT INTO `songs` VALUES (1,'Mater\'s the Bomb',1,1,197,'placeholder',1),(2,'Towkyo Takeout',1,1,340,'placeholder',0),(3,'It\'s Finn McMissile!',1,1,354,'placeholder',0),(4,'Tarmac the Magnificent',1,1,159,'placeholder',0),(5,'Blunder and Lightning',1,1,137,'placeholder',0),(6,'Graduation',2,3,193,'placeholder',0),(7,'The Pollen Jocks',2,3,92,'placeholder',0),(8,'Rooftop Consequences',2,3,110,'placeholder',0),(9,'Barry Turns the Screws',2,3,192,'placeholder',0),(10,'Assault on Honey Farms',2,3,153,'placeholder',0),(11,'Corelia Chase',4,4,214,'placeholder',0),(12,'Gonna Be aAPilot',3,4,29,'placeholder',0),(13,'L3 & Millenium Falcon',4,4,196,'placeholder',0),(14,'Double-Double Cross',4,4,287,'placeholder',0),(15,'Spaceport',4,4,249,'placeholder',0),(16,'Casey\'s Song',5,5,117,'placeholder',0),(17,'Drum Battle',5,5,130,'placeholder',0),(18,'Overture',5,5,199,'placeholder',0),(19,'Too Hip To Retire',5,5,184,'placeholder',0),(20,'Dismissed',5,5,166,'placeholder',0),(21,'test song',1,1,2,'1',1),(23,'test',1,1,1,'test',0),(24,'test',1,1,1,'1',0),(25,'test',1,1,420,'test',1),(26,'test',1,1,420,'test',1),(27,'test',1,1,1,'test',0),(28,'test',1,1,1,'oiszfj',0);
/*!40000 ALTER TABLE `songs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `songs_log`
--

DROP TABLE IF EXISTS `songs_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `songs_log` (
  `user` varchar(50) DEFAULT NULL,
  `action_type` varchar(10) NOT NULL,
  `action` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `songs_log`
--

LOCK TABLES `songs_log` WRITE;
/*!40000 ALTER TABLE `songs_log` DISABLE KEYS */;
INSERT INTO `songs_log` VALUES ('christofuy','Insert','Inserted song with name: test'),('christofuy','Insert','Inserted song with name: test'),('christofuy','Insert','Inserted song with name: test'),('christofuy','Insert','Inserted song with name: test'),('christofuy','Insert','Inserted song with id: 27'),('christofuy','Insert','Updated song with id: 25'),('christofuy','Delete','Deleted song with id: 25'),('christofuy','Insert','Inserted song with id: 28'),('christofuy','Update','Updated song with id: 26'),('christofuy','Delete','Deleted song with id: 26');
/*!40000 ALTER TABLE `songs_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `songs_with_composer_movie`
--

DROP TABLE IF EXISTS `songs_with_composer_movie`;
/*!50001 DROP VIEW IF EXISTS `songs_with_composer_movie`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `songs_with_composer_movie` AS SELECT 
 1 AS `songID`,
 1 AS `songName`,
 1 AS `composerID`,
 1 AS `movieID`,
 1 AS `songLength`,
 1 AS `ConnorsIncrediblyProfessionalAndPurelyObjectiveRating`,
 1 AS `deleted`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `studios`
--

DROP TABLE IF EXISTS `studios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studios` (
  `studioID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `location` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`studioID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studios`
--

LOCK TABLES `studios` WRITE;
/*!40000 ALTER TABLE `studios` DISABLE KEYS */;
INSERT INTO `studios` VALUES (1,'Walt Disney Studios','Burbank, California'),(2,'A Band Apart','Los Angeles, California'),(3,'DreamWorks SKG','Glendale, California'),(4,'Lucasfilm Ltd.','San Francisco, California'),(5,'Blumhouse','Los Angeles, California');
/*!40000 ALTER TABLE `studios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studios_log`
--

DROP TABLE IF EXISTS `studios_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studios_log` (
  `user` varchar(50) DEFAULT NULL,
  `action` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studios_log`
--

LOCK TABLES `studios_log` WRITE;
/*!40000 ALTER TABLE `studios_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `studios_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `generalizedactorsview`
--

/*!50001 DROP VIEW IF EXISTS `generalizedactorsview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `generalizedactorsview` AS select `songs`.`songName` AS `songName`,`songs`.`songLength` AS `songLength`,`songs`.`ConnorsIncrediblyProfessionalAndPurelyObjectiveRating` AS `ConnorsIncrediblyProfessionalAndPurelyObjectiveRating` from `songs` where (`songs`.`deleted` = 0) order by rand() */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `generalizedcomposersview`
--

/*!50001 DROP VIEW IF EXISTS `generalizedcomposersview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `generalizedcomposersview` AS select `composers`.`name` AS `name`,`composers`.`age` AS `age` from `composers` order by rand() */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `generalizeddirectorsview`
--

/*!50001 DROP VIEW IF EXISTS `generalizeddirectorsview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `generalizeddirectorsview` AS select `directors`.`name` AS `name`,`directors`.`age` AS `age` from `directors` order by rand() */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `generalizedmoviesview`
--

/*!50001 DROP VIEW IF EXISTS `generalizedmoviesview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `generalizedmoviesview` AS select `movies`.`name` AS `name`,`movies`.`runtime` AS `runtime`,`movies`.`budget` AS `budget`,`movies`.`grossProfit` AS `grossProfit`,`movies`.`genre` AS `genre`,`movies`.`year` AS `year`,`movies`.`pSafeRating` AS `pSafeRating` from `movies` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `generalizedreviewsview`
--

/*!50001 DROP VIEW IF EXISTS `generalizedreviewsview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `generalizedreviewsview` AS select `reviews`.`username` AS `username`,`movies`.`name` AS `name`,`reviews`.`score` AS `score`,`reviews`.`text` AS `text` from (`reviews` join `movies` on((`movies`.`movieID` = `reviews`.`movieID`))) where (`reviews`.`deleted` = 0) order by rand() */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `generalizedsongsview`
--

/*!50001 DROP VIEW IF EXISTS `generalizedsongsview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `generalizedsongsview` AS select `songs`.`songName` AS `songName`,`songs`.`songLength` AS `songLength`,`songs`.`ConnorsIncrediblyProfessionalAndPurelyObjectiveRating` AS `ConnorsIncrediblyProfessionalAndPurelyObjectiveRating` from `songs` order by rand() */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `generalizedstudiosview`
--

/*!50001 DROP VIEW IF EXISTS `generalizedstudiosview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `generalizedstudiosview` AS select `studios`.`name` AS `name`,`studios`.`location` AS `location` from `studios` order by rand() */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `movies_with_director_composer_studio`
--

/*!50001 DROP VIEW IF EXISTS `movies_with_director_composer_studio`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `movies_with_director_composer_studio` AS select `m`.`movieID` AS `movieID`,`m`.`name` AS `movieName`,`m`.`directorID` AS `directorID`,`m`.`composerID` AS `composerID`,`m`.`studioID` AS `studioID`,`m`.`runtime` AS `runtime`,`m`.`budget` AS `budget`,`m`.`grossProfit` AS `grossProfit`,`m`.`criticScore` AS `criticScore`,`m`.`viewerScore` AS `viewerScore`,`m`.`genre` AS `genre`,`m`.`year` AS `year`,`m`.`nominatedForAward` AS `nominatedForAward`,`m`.`pSafeRating` AS `pSafeRating`,`d`.`name` AS `directorName`,`d`.`age` AS `directorAge`,`c`.`name` AS `composerName`,`c`.`age` AS `composerAge`,`c`.`movieCount` AS `composerMovieCount`,`s`.`name` AS `studioName`,`s`.`location` AS `studioLocation` from (((`movies` `m` join `directors` `d` on((`m`.`directorID` = `d`.`directorID`))) join `composers` `c` on((`m`.`composerID` = `c`.`composerID`))) join `studios` `s` on((`m`.`studioID` = `s`.`studioID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `songs_with_composer_movie`
--

/*!50001 DROP VIEW IF EXISTS `songs_with_composer_movie`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `songs_with_composer_movie` AS select `s`.`songID` AS `songID`,`s`.`songName` AS `songName`,`s`.`composerID` AS `composerID`,`s`.`movieID` AS `movieID`,`s`.`songLength` AS `songLength`,`s`.`ConnorsIncrediblyProfessionalAndPurelyObjectiveRating` AS `ConnorsIncrediblyProfessionalAndPurelyObjectiveRating`,`s`.`deleted` AS `deleted` from `songs` `s` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-17 13:58:38
