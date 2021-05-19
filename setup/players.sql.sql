-- MySQL dump 10.13  Distrib 8.0.24, for Win64 (x86_64)
--
-- Host: localhost    Database: faceit
-- ------------------------------------------------------
-- Server version	8.0.24

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
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `players` (
  `playerId` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `skillLevel` varchar(255) DEFAULT NULL,
  `faceitElo` varchar(255) DEFAULT NULL,
  `steamProfile` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`playerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES ('158f23b1-1e62-43a8-a24a-a20821a6e756','k1to0','https://assets.faceit-cdn.net/avatars/158f23b1-1e62-43a8-a24a-a20821a6e756_1550407318784.jpg','de','10','3615','76561198182462587'),('16316c98-371d-4585-bc8c-a77b82d2ba95','Dosia','https://assets.faceit-cdn.net/avatars/16316c98-371d-4585-bc8c-a77b82d2ba95_1550488846991.png','ru','10','3495','76561198106907258'),('19606e0c-137b-4885-a904-744fa12d25f6','niko','https://assets.faceit-cdn.net/avatars/19606e0c-137b-4885-a904-744fa12d25f6_1550490117189.jpg','ba','10','4018','76561198041683378'),('1cc20116-6b1c-44c0-b130-a828890cb7d2','xRogos','https://assets.faceit-cdn.net/avatars/1cc20116-6b1c-44c0-b130-a828890cb7d2_1612820114335.jpg','pl','10','2284','76561198167517681'),('26fc6f28-4374-4339-9b5e-01a26340fb12','Pimp','https://assets.faceit-cdn.net/avatars/26fc6f28-4374-4339-9b5e-01a26340fb12_1610489147858.jpg','dk','10','2650','76561198018008308'),('32fe0c33-f1ae-4c25-be94-f38eec8bb394','syrsoN','https://img.favpng.com/8/24/4/avatar-royalty-free-png-favpng-6920SU0BFdaEZTMCMSsrTTPws.jpg','de','10','3740','76561197980122997'),('3371d397-c2ee-4a1d-972f-54b8a7dd5238','RachelR','https://assets.faceit-cdn.net/avatars/3371d397-c2ee-4a1d-972f-54b8a7dd5238_1618568161336.jpg','ru','10','2594','76561198019889413'),('3872605b-2ed3-47a3-85d0-f47c466fcb74','Shawn_Cena','https://assets.faceit-cdn.net/avatars/3872605b-2ed3-47a3-85d0-f47c466fcb74_1550848323061.png','de','3','991','76561198218810765'),('38781beb-cab9-4291-a65a-84ea74f49843','Swanii','https://assets.faceit-cdn.net/avatars/38781beb-cab9-4291-a65a-84ea74f49843_1615724167065.jpg','de','10','2120','76561198071187674'),('3c2a0a29-6c01-485a-9b0d-0e6dfe8648b0','LobaIsLove','https://assets.faceit-cdn.net/avatars/3c2a0a29-6c01-485a-9b0d-0e6dfe8648b0_1605296115445.jpg','me','10','3769','76561198133274020'),('3f005401-8032-4112-abc8-f83d920eb258','tabseN','https://img.favpng.com/8/24/4/avatar-royalty-free-png-favpng-6920SU0BFdaEZTMCMSsrTTPws.jpg','de','10','3736','76561197961491680'),('47946790-c6fa-49c6-a29c-8667ed9e656e','olofmeister','https://assets.faceit-cdn.net/avatars/47946790-c6fa-49c6-a29c-8667ed9e656e_1550488606089.jpg','se','10','3266','76561197988627193'),('4946fdbd-00e9-4408-91dd-6f3c87c39b23','JW','https://assets.faceit-cdn.net/avatars/4946fdbd-00e9-4408-91dd-6f3c87c39b23_1582047085857.jpg','se','10','3358','76561198031554200'),('5c90ca92-7ea3-4b0c-b2cb-25edb5c6b77d','flusha','https://assets.faceit-cdn.net/avatars/5c90ca92-7ea3-4b0c-b2cb-25edb5c6b77d_1553256462906.jpg','se','10','3515','76561197991348083'),('5cd2827e-9f73-4080-8cb2-82bee817a173','Xyp9x','https://assets.faceit-cdn.net/avatars/5cd2827e-9f73-4080-8cb2-82bee817a173_1550489182347.jpg','dk','10','4066','76561197990682262'),('5e0a2741-f8cd-43ec-8033-c27d9af900cb','fknflash','https://assets.faceit-cdn.net/avatars/5e0a2741-f8cd-43ec-8033-c27d9af900cb_1609262570726.jpg','de','3','1088','76561198088332583'),('61703d90-82f7-4fb7-97b4-adb1c300f624','TrilluXe','https://assets.faceit-cdn.net/avatars/61703d90-82f7-4fb7-97b4-adb1c300f624_1550505907339.jpg','de','7','1690','76561198021323440'),('7e80ed2a-8e39-457e-95c2-1c9ba9449daf','dupreeh','https://assets.faceit-cdn.net/avatars/7e80ed2a-8e39-457e-95c2-1c9ba9449daf_1619633430489.jpg','dk','10','3670','76561198004854956'),('9269548a-6cd4-46a7-a3b8-9f3816e52e49','kennyS-','https://assets.faceit-cdn.net/avatars/9269548a-6cd4-46a7-a3b8-9f3816e52e49_1550509361832.jpg','fr','10','3397','76561198024905796'),('936a539c-ef03-4fb2-b5d6-97218f5d464d','JACKZ','https://assets.faceit-cdn.net/avatars/936a539c-ef03-4fb2-b5d6-97218f5d464d_1591122007429.jpg','fr','10','3252','76561197972242917'),('d6bc4849-5256-4463-a38e-bcd77fc31ff9','device','https://assets.faceit-cdn.net/avatars/d6bc4849-5256-4463-a38e-bcd77fc31ff9_1550488577898.jpg','dk','10','3470','76561197987713664'),('db19b0d5-0ac2-43a9-99a3-a78613d9d385','XANTARES','https://assets.faceit-cdn.net/avatars/db19b0d5-0ac2-43a9-99a3-a78613d9d385_1553476122162.jpg','tr','10','3900','76561198044118796'),('de21905f-47e9-46c2-bfd2-e56f63795c87','apEX','https://assets.faceit-cdn.net/avatars/de21905f-47e9-46c2-bfd2-e56f63795c87_1590152113676.jpg','fr','10','3446','76561197989744167'),('f8bd2fd4-1860-441e-8851-3469dd3a1a55','tiziaN','https://assets.faceit-cdn.net/avatars/f8bd2fd4-1860-441e-8851-3469dd3a1a55_1594408782311.jpg','de','10','3517','76561197997556936'),('f955ee63-cd49-4803-b57b-f3df2480e21a','BubzkjiXD','https://assets.faceit-cdn.net/avatars/f955ee63-cd49-4803-b57b-f3df2480e21a_1616018982634.jpg','dk','10','3649','76561198131369187');
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-19 19:08:11
