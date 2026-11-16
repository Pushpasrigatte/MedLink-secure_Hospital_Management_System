-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: bujji
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admins` (
  `custom_id` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `access_level` varchar(50) NOT NULL,
  `gender` enum('male','female','other') NOT NULL,
  `email` varchar(50) NOT NULL,
  `contact_number` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `public_key_e` bigint(20) DEFAULT NULL,
  `private_key_d` bigint(20) DEFAULT NULL,
  `modulus_n` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`custom_id`),
  UNIQUE KEY `custom_id` (`custom_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `contact_number` (`contact_number`),
  CONSTRAINT `chk_admin_password_length` CHECK (char_length(`password`) between 6 and 20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES ('A25A0001','yuktha','full','female','yuktha@gmail.com','+917788994455','yuktha121',NULL,NULL,NULL),('A25A0002','visali','full','female','visalakshi@gmail.com','+917894561230','9876543210',NULL,NULL,NULL);
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor_lab_reply_messages`
--

DROP TABLE IF EXISTS `doctor_lab_reply_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `doctor_lab_reply_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doctor_id` varchar(20) NOT NULL,
  `lab_id` varchar(20) NOT NULL,
  `reply_text` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `encrypted_message` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `lab_id` (`lab_id`),
  CONSTRAINT `doctor_lab_reply_messages_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`custom_id`),
  CONSTRAINT `doctor_lab_reply_messages_ibfk_2` FOREIGN KEY (`lab_id`) REFERENCES `labs` (`custom_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_lab_reply_messages`
--

LOCK TABLES `doctor_lab_reply_messages` WRITE;
/*!40000 ALTER TABLE `doctor_lab_reply_messages` DISABLE KEYS */;
INSERT INTO `doctor_lab_reply_messages` VALUES (1,'D25A0001','L25A0002','yes please tell me','2025-06-30 17:23:09',NULL);
/*!40000 ALTER TABLE `doctor_lab_reply_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `doctors` (
  `custom_id` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `specialization` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `experience` varchar(50) NOT NULL,
  `gender` enum('male','female','other') NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `public_key_e` bigint(20) DEFAULT NULL,
  `private_key_d` bigint(20) DEFAULT NULL,
  `modulus_n` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`custom_id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `chk_doctor_password_length` CHECK (char_length(`password`) between 6 and 20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES ('D25A0001','komalatha','dentist','+919705573880','1','female','komalatha.adapa123@gmail.com','9705573880',NULL,NULL,NULL),('D25A0002','venkatreddy','heart','+919866205013','12','male','venkatareddy112@gmail.com','123456',NULL,NULL,NULL),('D25A0003','venkatareddy','cardiac','+919866205010','11','male','venkatareddyy112@gmail.com','9876543210',NULL,NULL,NULL);
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospitals`
--

DROP TABLE IF EXISTS `hospitals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hospitals` (
  `custom_id` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `designation` varchar(100) NOT NULL,
  `gender` enum('male','female','other') NOT NULL,
  `email` varchar(50) NOT NULL,
  `contact_number` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `public_key_e` bigint(20) DEFAULT NULL,
  `private_key_d` bigint(20) DEFAULT NULL,
  `modulus_n` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`custom_id`),
  UNIQUE KEY `contact_number` (`contact_number`),
  CONSTRAINT `chk_hospital_password_length` CHECK (char_length(`password`) between 6 and 20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospitals`
--

LOCK TABLES `hospitals` WRITE;
/*!40000 ALTER TABLE `hospitals` DISABLE KEYS */;
INSERT INTO `hospitals` VALUES ('H25A0001','Gatte Pushpasri','attendant','female','pushpasrigatte@gmail.com','+918247079226','0147852',NULL,NULL,NULL),('H25A0002','saivamsi','receptionist','male','saivamsi@gmail.com','+917788996622','saivamsi12',NULL,NULL,NULL);
/*!40000 ALTER TABLE `hospitals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lab_doctor_messages`
--

DROP TABLE IF EXISTS `lab_doctor_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lab_doctor_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lab_id` varchar(20) DEFAULT NULL,
  `doctor_id` varchar(20) DEFAULT NULL,
  `encrypted_message` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `lab_id` (`lab_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `lab_doctor_messages_ibfk_1` FOREIGN KEY (`lab_id`) REFERENCES `labs` (`custom_id`),
  CONSTRAINT `lab_doctor_messages_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`custom_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lab_doctor_messages`
--

LOCK TABLES `lab_doctor_messages` WRITE;
/*!40000 ALTER TABLE `lab_doctor_messages` DISABLE KEYS */;
INSERT INTO `lab_doctor_messages` VALUES (2,'L25A0002','D25A0001','gAAAAABoYsfYXK2cPX5rnzEjDrxMTax32EQ4TT3qdG_c8mAFVYIEWsVmnalQXuzghfhOsLXQ3z6HPnsA4UBKbM25onyrm42nTw==','2025-06-30 17:22:32');
/*!40000 ALTER TABLE `lab_doctor_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lab_image_messages`
--

DROP TABLE IF EXISTS `lab_image_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lab_image_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lab_id` varchar(20) NOT NULL,
  `doctor_id` varchar(20) NOT NULL,
  `image_path` varchar(200) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `lab_id` (`lab_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `lab_image_messages_ibfk_1` FOREIGN KEY (`lab_id`) REFERENCES `labs` (`custom_id`),
  CONSTRAINT `lab_image_messages_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`custom_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lab_image_messages`
--

LOCK TABLES `lab_image_messages` WRITE;
/*!40000 ALTER TABLE `lab_image_messages` DISABLE KEYS */;
INSERT INTO `lab_image_messages` VALUES (1,'L25A0002','D25A0001','static/uploads\\L25A0002_20250701093012_IMG-20231226-WA0012.jpg','2025-07-01 09:30:12');
/*!40000 ALTER TABLE `lab_image_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labs`
--

DROP TABLE IF EXISTS `labs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `labs` (
  `custom_id` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `location` text NOT NULL,
  `gender` enum('male','female','other') NOT NULL,
  `email` varchar(50) NOT NULL,
  `contact_number` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `public_key_e` bigint(20) DEFAULT NULL,
  `private_key_d` bigint(20) DEFAULT NULL,
  `modulus_n` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`custom_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `contact_number` (`contact_number`),
  CONSTRAINT `chk_lab_password_length` CHECK (char_length(`password`) between 6 and 20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labs`
--

LOCK TABLES `labs` WRITE;
/*!40000 ALTER TABLE `labs` DISABLE KEYS */;
INSERT INTO `labs` VALUES ('L25A0001','pushpa','pochampally road,hyd','female','pushpa123@gmail.com','+919786453120','9786453120',NULL,NULL,NULL),('L25A0002','janu','pothavarappadu ,gopalapuram bus stop nunna rd','female','janu123@gmail.com','+917785599447','janu143',NULL,NULL,NULL);
/*!40000 ALTER TABLE `labs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` varchar(20) NOT NULL,
  `receiver_id` varchar(20) NOT NULL,
  `sender_role` varchar(20) NOT NULL,
  `receiver_role` varchar(20) NOT NULL,
  `encrypted_message` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_doctor_messages`
--

DROP TABLE IF EXISTS `patient_doctor_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient_doctor_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(20) DEFAULT NULL,
  `doctor_id` varchar(20) DEFAULT NULL,
  `encrypted_message` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `reply_text` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `patient_doctor_messages_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`custom_id`),
  CONSTRAINT `patient_doctor_messages_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`custom_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_doctor_messages`
--

LOCK TABLES `patient_doctor_messages` WRITE;
/*!40000 ALTER TABLE `patient_doctor_messages` DISABLE KEYS */;
INSERT INTO `patient_doctor_messages` VALUES (1,'P25A0001','D25A0001','gAAAAABoY6o7sQsg0sCwH9leQ6iP5u3-dtGa39S3jAIMKD9BOaQCqCDilukoafrY065dHF7lVaP4eOz25MFF26ofPMSgB_iI9WVD7vk9jvFL4sgafimj2FWrprlKAH_mlFQtdbB8yQWs','2025-07-01 09:28:27','meet me at 12 o clock');
/*!40000 ALTER TABLE `patient_doctor_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_doctor_reply_messages`
--

DROP TABLE IF EXISTS `patient_doctor_reply_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient_doctor_reply_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doctor_id` varchar(20) DEFAULT NULL,
  `patient_id` varchar(20) DEFAULT NULL,
  `encrypted_message` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `patient_doctor_reply_messages_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`custom_id`),
  CONSTRAINT `patient_doctor_reply_messages_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`custom_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_doctor_reply_messages`
--

LOCK TABLES `patient_doctor_reply_messages` WRITE;
/*!40000 ALTER TABLE `patient_doctor_reply_messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `patient_doctor_reply_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_image_messages`
--

DROP TABLE IF EXISTS `patient_image_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient_image_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(20) NOT NULL,
  `doctor_id` varchar(20) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `patient_image_messages_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`custom_id`),
  CONSTRAINT `patient_image_messages_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`custom_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_image_messages`
--

LOCK TABLES `patient_image_messages` WRITE;
/*!40000 ALTER TABLE `patient_image_messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `patient_image_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_images`
--

DROP TABLE IF EXISTS `patient_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(20) NOT NULL,
  `image_path` varchar(200) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `patient_images_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`custom_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_images`
--

LOCK TABLES `patient_images` WRITE;
/*!40000 ALTER TABLE `patient_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `patient_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patients` (
  `custom_id` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `gender` enum('male','female','other') NOT NULL,
  `age` int(11) NOT NULL,
  `contact_number` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `public_key_e` bigint(20) DEFAULT NULL,
  `private_key_d` bigint(20) DEFAULT NULL,
  `modulus_n` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`custom_id`),
  UNIQUE KEY `contact_number` (`contact_number`),
  CONSTRAINT `chk_patient_password_length` CHECK (char_length(`password`) between 6 and 20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES ('P25A0001','komalatha adapa','female',20,'+919705573330','komalathaadapa@gmail.com','9705573330',NULL,NULL,NULL),('P25A0002','sangu jahnavi','female',21,'+919876543210','sangujahnavireddy@gmail.com','9876543210',NULL,NULL,NULL),('P25A0003','Komali','female',20,'+919705573880','Komali.123@gmail.com','12345678-A',NULL,NULL,NULL);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-01 15:20:52
