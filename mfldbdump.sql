-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: mfl_interface_db
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--
DROP DATABASE IF EXISTS mfl_interface_db;
CREATE DATABASE mfl_interface_db;
CREATE DATABASE hickory_smoke;

USE mfl_interface_db;

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add counties',1,'add_counties'),(2,'Can change counties',1,'change_counties'),(3,'Can delete counties',1,'delete_counties'),(4,'Can view counties',1,'view_counties'),(5,'Can add em r_type',2,'add_emr_type'),(6,'Can change em r_type',2,'change_emr_type'),(7,'Can delete em r_type',2,'delete_emr_type'),(8,'Can view em r_type',2,'view_emr_type'),(9,'Can add facility_ info',3,'add_facility_info'),(10,'Can change facility_ info',3,'change_facility_info'),(11,'Can delete facility_ info',3,'delete_facility_info'),(12,'Can view facility_ info',3,'view_facility_info'),(13,'Can add ht s_deployment_type',4,'add_hts_deployment_type'),(14,'Can change ht s_deployment_type',4,'change_hts_deployment_type'),(15,'Can delete ht s_deployment_type',4,'delete_hts_deployment_type'),(16,'Can view ht s_deployment_type',4,'view_hts_deployment_type'),(17,'Can add ht s_use_type',5,'add_hts_use_type'),(18,'Can change ht s_use_type',5,'change_hts_use_type'),(19,'Can delete ht s_use_type',5,'delete_hts_use_type'),(20,'Can view ht s_use_type',5,'view_hts_use_type'),(21,'Can add i pdata',6,'add_ipdata'),(22,'Can change i pdata',6,'change_ipdata'),(23,'Can delete i pdata',6,'delete_ipdata'),(24,'Can view i pdata',6,'view_ipdata'),(25,'Can add owner',7,'add_owner'),(26,'Can change owner',7,'change_owner'),(27,'Can delete owner',7,'delete_owner'),(28,'Can view owner',7,'view_owner'),(29,'Can add sd p_agencies',8,'add_sdp_agencies'),(30,'Can change sd p_agencies',8,'change_sdp_agencies'),(31,'Can delete sd p_agencies',8,'delete_sdp_agencies'),(32,'Can view sd p_agencies',8,'view_sdp_agencies'),(33,'Can add sub_counties',9,'add_sub_counties'),(34,'Can change sub_counties',9,'change_sub_counties'),(35,'Can delete sub_counties',9,'delete_sub_counties'),(36,'Can view sub_counties',9,'view_sub_counties'),(37,'Can add partners',10,'add_partners'),(38,'Can change partners',10,'change_partners'),(39,'Can delete partners',10,'delete_partners'),(40,'Can view partners',10,'view_partners'),(41,'Can add m health_ info',11,'add_mhealth_info'),(42,'Can change m health_ info',11,'change_mhealth_info'),(43,'Can delete m health_ info',11,'delete_mhealth_info'),(44,'Can view m health_ info',11,'view_mhealth_info'),(45,'Can add implementation_type',12,'add_implementation_type'),(46,'Can change implementation_type',12,'change_implementation_type'),(47,'Can delete implementation_type',12,'delete_implementation_type'),(48,'Can view implementation_type',12,'view_implementation_type'),(49,'Can add i l_ info',13,'add_il_info'),(50,'Can change i l_ info',13,'change_il_info'),(51,'Can delete i l_ info',13,'delete_il_info'),(52,'Can view i l_ info',13,'view_il_info'),(53,'Can add ht s_ info',14,'add_hts_info'),(54,'Can change ht s_ info',14,'change_hts_info'),(55,'Can delete ht s_ info',14,'delete_hts_info'),(56,'Can view ht s_ info',14,'view_hts_info'),(57,'Can add em r_ info',15,'add_emr_info'),(58,'Can change em r_ info',15,'change_emr_info'),(59,'Can delete em r_ info',15,'delete_emr_info'),(60,'Can view em r_ info',15,'view_emr_info'),(61,'Can add log entry',16,'add_logentry'),(62,'Can change log entry',16,'change_logentry'),(63,'Can delete log entry',16,'delete_logentry'),(64,'Can view log entry',16,'view_logentry'),(65,'Can add permission',17,'add_permission'),(66,'Can change permission',17,'change_permission'),(67,'Can delete permission',17,'delete_permission'),(68,'Can view permission',17,'view_permission'),(69,'Can add group',18,'add_group'),(70,'Can change group',18,'change_group'),(71,'Can delete group',18,'delete_group'),(72,'Can view group',18,'view_group'),(73,'Can add user',19,'add_user'),(74,'Can change user',19,'change_user'),(75,'Can delete user',19,'delete_user'),(76,'Can view user',19,'view_user'),(77,'Can add content type',20,'add_contenttype'),(78,'Can change content type',20,'change_contenttype'),(79,'Can delete content type',20,'delete_contenttype'),(80,'Can view content type',20,'view_contenttype'),(81,'Can add session',21,'add_session'),(82,'Can change session',21,'change_session'),(83,'Can delete session',21,'delete_session'),(84,'Can view session',21,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$320000$OCXkyz23PvawCTSlCCmdW7$bSbLEGH5ExECwLCIRMsEoOcWgbw509jB1L095CcVrU0=','2022-02-08 21:21:04.394416',1,'marykils','','','marykilewe@gmail.com',1,1,'2022-02-08 20:36:45.605702'),(2,'pbkdf2_sha256$320000$5FDM23KaOeYdAKlSlQaF4v$YpPPgPX+ScU8+zKjhsKmy1ymZ06ahQBMDRC8wiUBv/o=',NULL,0,'test','','','',0,1,'2022-02-08 20:49:30.013418'),(3,'pbkdf2_sha256$320000$W16sFrDZlRXQZc4i2PQSZN$qa0MrJOqAmlmsNpjiwQI0tFV5i7SO4G0kGQhKWaJzVA=','2022-02-09 14:34:08.500410',0,'hushpuppy','hush','puppy','hushpuppy@gmail.com',0,1,'2022-02-08 20:57:15.237756');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (16,'admin','logentry'),(18,'auth','group'),(17,'auth','permission'),(19,'auth','user'),(20,'contenttypes','contenttype'),(1,'facilities','counties'),(15,'facilities','emr_info'),(2,'facilities','emr_type'),(3,'facilities','facility_info'),(4,'facilities','hts_deployment_type'),(14,'facilities','hts_info'),(5,'facilities','hts_use_type'),(13,'facilities','il_info'),(12,'facilities','implementation_type'),(6,'facilities','ipdata'),(11,'facilities','mhealth_info'),(7,'facilities','owner'),(10,'facilities','partners'),(8,'facilities','sdp_agencies'),(9,'facilities','sub_counties'),(21,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2022-02-07 15:09:20.118903'),(2,'auth','0001_initial','2022-02-07 15:09:21.071094'),(3,'admin','0001_initial','2022-02-07 15:09:21.285557'),(4,'admin','0002_logentry_remove_auto_add','2022-02-07 15:09:21.293559'),(5,'admin','0003_logentry_add_action_flag_choices','2022-02-07 15:09:21.301823'),(6,'contenttypes','0002_remove_content_type_name','2022-02-07 15:09:21.451278'),(7,'auth','0002_alter_permission_name_max_length','2022-02-07 15:09:21.559006'),(8,'auth','0003_alter_user_email_max_length','2022-02-07 15:09:21.611395'),(9,'auth','0004_alter_user_username_opts','2022-02-07 15:09:21.625826'),(10,'auth','0005_alter_user_last_login_null','2022-02-07 15:09:21.993779'),(11,'auth','0006_require_contenttypes_0002','2022-02-07 15:09:21.993779'),(12,'auth','0007_alter_validators_add_error_messages','2022-02-07 15:09:22.009700'),(13,'auth','0008_alter_user_username_max_length','2022-02-07 15:09:22.137303'),(14,'auth','0009_alter_user_last_name_max_length','2022-02-07 15:09:22.218711'),(15,'auth','0010_alter_group_name_max_length','2022-02-07 15:09:22.243826'),(16,'auth','0011_update_proxy_permissions','2022-02-07 15:09:22.252621'),(17,'auth','0012_alter_user_first_name_max_length','2022-02-07 15:09:22.342367'),(18,'facilities','0001_initial','2022-02-07 15:09:24.471478'),(19,'sessions','0001_initial','2022-02-07 15:09:24.624807'),(20,'facilities','0002_remove_facility_info_implementation','2022-02-07 15:32:00.860595'),(21,'facilities','0003_remove_mhealth_info_otz_remove_mhealth_info_ovc_and_more','2022-02-08 19:09:10.138840');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('nrgxww9u4le15hp9ircmubkpkl001fkr','.eJxVjEEOwiAQRe_C2pDSMlNw6b5nIAMMUjWQlHZlvLtt0oVu33v_v4Wjbc1ua7y4OYqrGMTll3kKTy6HiA8q9ypDLesye3kk8rRNTjXy63a2fweZWt7XxAiIsRto0H0yFliB8qDDjrhHy4G7EUkFDaRSMsaj9dYEZjVGQhCfL95IOA8:1nHo2q:AuBisbacJFHfbMPsw0rrO9D19epyN-OHhFaRoKf5gtI','2022-02-23 14:34:08.507510');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_counties`
--

DROP TABLE IF EXISTS `facilities_counties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_counties` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_counties`
--

LOCK TABLES `facilities_counties` WRITE;
/*!40000 ALTER TABLE `facilities_counties` DISABLE KEYS */;
INSERT INTO `facilities_counties` VALUES (1,'Mombasa'),(2,'Kwale'),(3,'Kilifi'),(4,'Tana River'),(5,'Lamu'),(6,'Taita-Taveta'),(7,'Garissa'),(8,'Wajir'),(9,'Mandera'),(10,'Marsabit'),(11,'Isiolo'),(12,'Meru'),(13,'Tharaka-Nithi'),(14,'Embu'),(15,'Kitui'),(16,'Machakos'),(17,'Makueni'),(18,'Nyandarua'),(19,'Nyeri'),(20,'Kirinyaga'),(21,'Murang’a'),(22,'Kiambu'),(23,'Turkana'),(24,'West Pokot'),(25,'Samburu'),(26,'Trans Nzoia'),(27,'Uasin Gishu'),(28,'Elgeyo-Marakwet'),(29,'Nandi'),(30,'Baringo'),(31,'Laikipia'),(32,'Nakuru'),(33,'Narok'),(34,'Kajiado'),(35,'Kericho'),(36,'Bomet'),(37,'Kakamega'),(38,'Vihiga'),(39,'Bungoma'),(40,'Busia'),(41,'Siaya'),(42,'Kisumu'),(43,'Homa Bay'),(44,'Migori'),(45,'Kisii'),(46,'Nyamira'),(47,'Nairobi');
/*!40000 ALTER TABLE `facilities_counties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_emr_info`
--

DROP TABLE IF EXISTS `facilities_emr_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_emr_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(100) NOT NULL,
  `facility_info_id` char(32) NOT NULL,
  `type_id` bigint NOT NULL,
  `otz` varchar(10) NOT NULL,
  `ovc` varchar(10) NOT NULL,
  `prep` varchar(10) NOT NULL,
  `tb` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `facilities_emr_info_facility_info_id_60e47689_fk_facilitie` (`facility_info_id`),
  KEY `facilities_emr_info_type_id_4caed616_fk_facilities_emr_type_id` (`type_id`),
  CONSTRAINT `facilities_emr_info_facility_info_id_60e47689_fk_facilitie` FOREIGN KEY (`facility_info_id`) REFERENCES `facilities_facility_info` (`id`),
  CONSTRAINT `facilities_emr_info_type_id_4caed616_fk_facilities_emr_type_id` FOREIGN KEY (`type_id`) REFERENCES `facilities_emr_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_emr_info`
--

LOCK TABLES `facilities_emr_info` WRITE;
/*!40000 ALTER TABLE `facilities_emr_info` DISABLE KEYS */;
INSERT INTO `facilities_emr_info` VALUES (4,'Stalled/Inactive','965c121ac5b345baac44952ae92c8f2c',1,'Yes','Yes','No','No'),(5,'Active','f7138a9ca1d14dce8fcfd0d3ae655141',1,'Yes','Yes','No','No'),(6,'Active','cf8b50379a55415c97775496b0e94185',1,'No','No','Yes','Yes'),(7,'Active','3b06b5971c5943c9a62af5f4d73c66af',1,'No','No','No','No'),(8,'Active','1f4dcc62fd1141d5a2c5fbdeb21843f2',1,'Yes','Yes','Yes','Yes');
/*!40000 ALTER TABLE `facilities_emr_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_emr_type`
--

DROP TABLE IF EXISTS `facilities_emr_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_emr_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_emr_type`
--

LOCK TABLES `facilities_emr_type` WRITE;
/*!40000 ALTER TABLE `facilities_emr_type` DISABLE KEYS */;
INSERT INTO `facilities_emr_type` VALUES (1,'KenyaEMR'),(2,'IQCare-KeHMIS'),(3,'AMRS');
/*!40000 ALTER TABLE `facilities_emr_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_facility_info`
--

DROP TABLE IF EXISTS `facilities_facility_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_facility_info` (
  `id` char(32) NOT NULL,
  `mfl_code` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `lat` decimal(9,6) NOT NULL,
  `lon` decimal(9,6) NOT NULL,
  `county_id` bigint NOT NULL,
  `owner_id` bigint NOT NULL,
  `partner_id` bigint NOT NULL,
  `sub_county_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `facilities_facility__owner_id_d92ec1b4_fk_facilitie` (`owner_id`),
  KEY `facilities_facility__partner_id_74db8149_fk_facilitie` (`partner_id`),
  KEY `facilities_facility__sub_county_id_fb60feab_fk_facilitie` (`sub_county_id`),
  KEY `facilities_facility__county_id_164374dc_fk_facilitie` (`county_id`),
  CONSTRAINT `facilities_facility__county_id_164374dc_fk_facilitie` FOREIGN KEY (`county_id`) REFERENCES `facilities_counties` (`id`),
  CONSTRAINT `facilities_facility__owner_id_d92ec1b4_fk_facilitie` FOREIGN KEY (`owner_id`) REFERENCES `facilities_owner` (`id`),
  CONSTRAINT `facilities_facility__partner_id_74db8149_fk_facilitie` FOREIGN KEY (`partner_id`) REFERENCES `facilities_partners` (`id`),
  CONSTRAINT `facilities_facility__sub_county_id_fb60feab_fk_facilitie` FOREIGN KEY (`sub_county_id`) REFERENCES `facilities_sub_counties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_facility_info`
--

LOCK TABLES `facilities_facility_info` WRITE;
/*!40000 ALTER TABLE `facilities_facility_info` DISABLE KEYS */;
INSERT INTO `facilities_facility_info` VALUES ('1f4dcc62fd1141d5a2c5fbdeb21843f2',13486,'Arombe Dispensary',-1.034840,34.350830,44,2,2,6),('3b06b5971c5943c9a62af5f4d73c66af',13469,'Airport Health Centre',-0.073310,34.733590,42,4,4,4),('965c121ac5b345baac44952ae92c8f2c',14181,'3KR Health Center',-0.296560,36.145330,32,1,1,1),('cf8b50379a55415c97775496b0e94185',14178,'AIC Litein Mission Hospital',-0.586210,35.186500,35,3,3,3),('f7138a9ca1d14dce8fcfd0d3ae655141',13468,'Ahero County Hospital',2.000000,2.000000,42,1,1,5);
/*!40000 ALTER TABLE `facilities_facility_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_hts_deployment_type`
--

DROP TABLE IF EXISTS `facilities_hts_deployment_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_hts_deployment_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `deployment` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_hts_deployment_type`
--

LOCK TABLES `facilities_hts_deployment_type` WRITE;
/*!40000 ALTER TABLE `facilities_hts_deployment_type` DISABLE KEYS */;
INSERT INTO `facilities_hts_deployment_type` VALUES (1,'Mobile Only'),(2,'Desktop Only'),(3,'Hybrid'),(4,'N/A');
/*!40000 ALTER TABLE `facilities_hts_deployment_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_hts_info`
--

DROP TABLE IF EXISTS `facilities_hts_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_hts_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(100) NOT NULL,
  `deployment_id` bigint NOT NULL,
  `facility_info_id` char(32) NOT NULL,
  `hts_use_name_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `facilities_hts_info_deployment_id_d977e79b_fk_facilitie` (`deployment_id`),
  KEY `facilities_hts_info_facility_info_id_f6f63223_fk_facilitie` (`facility_info_id`),
  KEY `facilities_hts_info_hts_use_name_id_41a5cf51_fk_facilitie` (`hts_use_name_id`),
  CONSTRAINT `facilities_hts_info_deployment_id_d977e79b_fk_facilitie` FOREIGN KEY (`deployment_id`) REFERENCES `facilities_hts_deployment_type` (`id`),
  CONSTRAINT `facilities_hts_info_facility_info_id_f6f63223_fk_facilitie` FOREIGN KEY (`facility_info_id`) REFERENCES `facilities_facility_info` (`id`),
  CONSTRAINT `facilities_hts_info_hts_use_name_id_41a5cf51_fk_facilitie` FOREIGN KEY (`hts_use_name_id`) REFERENCES `facilities_hts_use_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_hts_info`
--

LOCK TABLES `facilities_hts_info` WRITE;
/*!40000 ALTER TABLE `facilities_hts_info` DISABLE KEYS */;
INSERT INTO `facilities_hts_info` VALUES (4,'N/A',4,'965c121ac5b345baac44952ae92c8f2c',4),(5,'Active',1,'f7138a9ca1d14dce8fcfd0d3ae655141',1),(6,'N/A',4,'cf8b50379a55415c97775496b0e94185',4),(7,'Active',2,'3b06b5971c5943c9a62af5f4d73c66af',2),(8,'Active',1,'1f4dcc62fd1141d5a2c5fbdeb21843f2',1);
/*!40000 ALTER TABLE `facilities_hts_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_hts_use_type`
--

DROP TABLE IF EXISTS `facilities_hts_use_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_hts_use_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `hts_use_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_hts_use_type`
--

LOCK TABLES `facilities_hts_use_type` WRITE;
/*!40000 ALTER TABLE `facilities_hts_use_type` DISABLE KEYS */;
INSERT INTO `facilities_hts_use_type` VALUES (1,'mUzima'),(2,'HTS Module'),(3,'AfyaSTAT'),(4,'No HTS Use'),(5,'N/A');
/*!40000 ALTER TABLE `facilities_hts_use_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_il_info`
--

DROP TABLE IF EXISTS `facilities_il_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_il_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(100) NOT NULL,
  `registration_ie` varchar(10) NOT NULL,
  `pharmacy_ie` varchar(10) NOT NULL,
  `facility_info_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `facilities_il_info_facility_info_id_26524a8d_fk_facilitie` (`facility_info_id`),
  CONSTRAINT `facilities_il_info_facility_info_id_26524a8d_fk_facilitie` FOREIGN KEY (`facility_info_id`) REFERENCES `facilities_facility_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_il_info`
--

LOCK TABLES `facilities_il_info` WRITE;
/*!40000 ALTER TABLE `facilities_il_info` DISABLE KEYS */;
INSERT INTO `facilities_il_info` VALUES (3,'N/A','N/A','N/A','965c121ac5b345baac44952ae92c8f2c'),(4,'N/A','No','No','f7138a9ca1d14dce8fcfd0d3ae655141'),(5,'N/A','No','No','cf8b50379a55415c97775496b0e94185'),(6,'N/A','No','No','3b06b5971c5943c9a62af5f4d73c66af'),(7,'Active','No','No','1f4dcc62fd1141d5a2c5fbdeb21843f2');
/*!40000 ALTER TABLE `facilities_il_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_implementation_type`
--

DROP TABLE IF EXISTS `facilities_implementation_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_implementation_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(100) NOT NULL,
  `ct` tinyint(1) NOT NULL,
  `hts` tinyint(1) NOT NULL,
  `il` tinyint(1) NOT NULL,
  `kp` tinyint(1) NOT NULL,
  `facility_info_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `facilities_implement_facility_info_id_992e76de_fk_facilitie` (`facility_info_id`),
  CONSTRAINT `facilities_implement_facility_info_id_992e76de_fk_facilitie` FOREIGN KEY (`facility_info_id`) REFERENCES `facilities_facility_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_implementation_type`
--

LOCK TABLES `facilities_implementation_type` WRITE;
/*!40000 ALTER TABLE `facilities_implementation_type` DISABLE KEYS */;
INSERT INTO `facilities_implementation_type` VALUES (5,'',1,0,0,0,'965c121ac5b345baac44952ae92c8f2c'),(6,'',1,1,0,0,'f7138a9ca1d14dce8fcfd0d3ae655141'),(7,'',1,0,0,0,'cf8b50379a55415c97775496b0e94185'),(8,'',1,1,0,0,'3b06b5971c5943c9a62af5f4d73c66af'),(9,'',1,1,1,0,'1f4dcc62fd1141d5a2c5fbdeb21843f2');
/*!40000 ALTER TABLE `facilities_implementation_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_ipdata`
--

DROP TABLE IF EXISTS `facilities_ipdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_ipdata` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `city` varchar(200) NOT NULL,
  `country` varchar(200) NOT NULL,
  `lat` decimal(9,6) NOT NULL,
  `lon` decimal(9,6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_ipdata`
--

LOCK TABLES `facilities_ipdata` WRITE;
/*!40000 ALTER TABLE `facilities_ipdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `facilities_ipdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_mhealth_info`
--

DROP TABLE IF EXISTS `facilities_mhealth_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_mhealth_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `facility_info_id` char(32) NOT NULL,
  `c4c` tinyint(1) NOT NULL,
  `mshauri` tinyint(1) NOT NULL,
  `nishauri` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `facilities_mhealth_i_facility_info_id_41c4b33d_fk_facilitie` (`facility_info_id`),
  CONSTRAINT `facilities_mhealth_i_facility_info_id_41c4b33d_fk_facilitie` FOREIGN KEY (`facility_info_id`) REFERENCES `facilities_facility_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_mhealth_info`
--

LOCK TABLES `facilities_mhealth_info` WRITE;
/*!40000 ALTER TABLE `facilities_mhealth_info` DISABLE KEYS */;
INSERT INTO `facilities_mhealth_info` VALUES (2,'965c121ac5b345baac44952ae92c8f2c',0,0,0),(3,'f7138a9ca1d14dce8fcfd0d3ae655141',0,1,0),(4,'cf8b50379a55415c97775496b0e94185',0,0,0),(5,'3b06b5971c5943c9a62af5f4d73c66af',1,0,0),(6,'1f4dcc62fd1141d5a2c5fbdeb21843f2',0,0,0);
/*!40000 ALTER TABLE `facilities_mhealth_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_owner`
--

DROP TABLE IF EXISTS `facilities_owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_owner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_owner`
--

LOCK TABLES `facilities_owner` WRITE;
/*!40000 ALTER TABLE `facilities_owner` DISABLE KEYS */;
INSERT INTO `facilities_owner` VALUES (1,'Armed Forces'),(2,'Ministry of Health'),(3,'Other Faith based'),(4,'Local Authority'),(5,'Non-Governmental Organisations');
/*!40000 ALTER TABLE `facilities_owner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_partners`
--

DROP TABLE IF EXISTS `facilities_partners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_partners` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `agency_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `facilities_partners_agency_id_075fac14_fk_facilitie` (`agency_id`),
  CONSTRAINT `facilities_partners_agency_id_075fac14_fk_facilitie` FOREIGN KEY (`agency_id`) REFERENCES `facilities_sdp_agencies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_partners`
--

LOCK TABLES `facilities_partners` WRITE;
/*!40000 ALTER TABLE `facilities_partners` DISABLE KEYS */;
INSERT INTO `facilities_partners` VALUES (1,'HJF-Nairobi',3),(2,'CIHEB ENTRENCH',1),(3,'HJF-South Rift Valley',3),(4,'USAID Boresha Jamii',2);
/*!40000 ALTER TABLE `facilities_partners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_sdp_agencies`
--

DROP TABLE IF EXISTS `facilities_sdp_agencies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_sdp_agencies` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_sdp_agencies`
--

LOCK TABLES `facilities_sdp_agencies` WRITE;
/*!40000 ALTER TABLE `facilities_sdp_agencies` DISABLE KEYS */;
INSERT INTO `facilities_sdp_agencies` VALUES (1,'CDC'),(2,'USAID'),(3,'DOD');
/*!40000 ALTER TABLE `facilities_sdp_agencies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_sub_counties`
--

DROP TABLE IF EXISTS `facilities_sub_counties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_sub_counties` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `county_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `facilities_sub_count_county_id_6a095cab_fk_facilitie` (`county_id`),
  CONSTRAINT `facilities_sub_count_county_id_6a095cab_fk_facilitie` FOREIGN KEY (`county_id`) REFERENCES `facilities_counties` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_sub_counties`
--

LOCK TABLES `facilities_sub_counties` WRITE;
/*!40000 ALTER TABLE `facilities_sub_counties` DISABLE KEYS */;
INSERT INTO `facilities_sub_counties` VALUES (1,'Nakuru East',32),(2,'Nyando',42),(3,'Bureti',35),(4,'Kisumu West',42),(5,'Central',42),(6,'Suna West',44),(7,'Awendo',44),(8,'Nyatike',44),(9,'Narok West',33),(10,'Laikipia East',31),(21,'Seme',42),(22,'Bomet Central',36),(23,'Nyamira',46),(24,'Kuria West',44),(25,'Kuria East',44),(26,'Uriri',44),(27,'Konoin',36),(28,'Chepalungu',36),(29,'Tinderet',29),(30,'Muhoroni',42),(31,'Emgwen',29),(32,'Borabu',46),(33,'Mosop ',29),(34,'Nyamira North',46),(35,'Transmara East',33),(36,'Masaba North',46),(37,'South Mugirango',45),(38,'Kipkelion West',35),(39,'Nyaribari Masaa',45),(40,'Manga',46),(41,'Gilgil',32),(42,'Bomachoge Chache',45),(43,'Kitutu Chache South',45),(44,'Bonchari',45),(45,'Sigowet/Soin',35),(46,'Sotik',36);
/*!40000 ALTER TABLE `facilities_sub_counties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'mfl_interface_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-10 12:40:18
