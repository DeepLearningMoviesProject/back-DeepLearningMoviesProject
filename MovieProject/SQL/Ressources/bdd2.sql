-- MySQL dump 10.13  Distrib 5.5.54, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: bdd
-- ------------------------------------------------------
-- Server version	5.5.54-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `MOVIE`
--

DROP TABLE IF EXISTS `MOVIE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MOVIE` (
  `ID` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MOVIE`
--

LOCK TABLES `MOVIE` WRITE;
/*!40000 ALTER TABLE `MOVIE` DISABLE KEYS */;
INSERT INTO `MOVIE` VALUES (10),(12),(15),(20),(22),(24),(25),(28);
/*!40000 ALTER TABLE `MOVIE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USER`
--

DROP TABLE IF EXISTS `USER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `USER` (
  `ID` int(11) NOT NULL,
  `NAME` text NOT NULL,
  `MAIL` text NOT NULL,
  `TMDBKEY` text NOT NULL,
  `PASSWORD` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER`
--

LOCK TABLES `USER` WRITE;
/*!40000 ALTER TABLE `USER` DISABLE KEYS */;
INSERT INTO `USER` VALUES (2,'Edwin Niogret','blabla@hotmail.com','dsd412tmdb','pw'),(3,'Julian Hattinguais','python@live.com','dsd412tmdb','monmotdepasse');
/*!40000 ALTER TABLE `USER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USERMOVIE`
--

DROP TABLE IF EXISTS `USERMOVIE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `USERMOVIE` (
  `IDUSER` int(11) NOT NULL,
  `IDMOVIE` int(11) NOT NULL,
  `LIKED` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`IDUSER`,`IDMOVIE`),
  KEY `IDMOVIE` (`IDMOVIE`),
  CONSTRAINT `USERMOVIE_ibfk_1` FOREIGN KEY (`IDUSER`) REFERENCES `USER` (`ID`),
  CONSTRAINT `USERMOVIE_ibfk_2` FOREIGN KEY (`IDMOVIE`) REFERENCES `MOVIE` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USERMOVIE`
--

LOCK TABLES `USERMOVIE` WRITE;
/*!40000 ALTER TABLE `USERMOVIE` DISABLE KEYS */;
INSERT INTO `USERMOVIE` VALUES (2,10,0),(2,12,1),(2,25,0),(2,28,0);
/*!40000 ALTER TABLE `USERMOVIE` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-02-21 19:39:00
