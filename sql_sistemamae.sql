-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: gestao
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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
-- Table structure for table `cheques`
--

DROP TABLE IF EXISTS `cheques`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cheques` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(50) NOT NULL,
  `valor` decimal(10,2) NOT NULL,
  `nome_destino` varchar(150) NOT NULL,
  `data_vencimento` date DEFAULT NULL,
  `status` enum('PENDENTE','COMPENSADO','SUSTADO','CANCELADO') DEFAULT NULL,
  `criado_em` timestamp NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cheques`
--

LOCK TABLES `cheques` WRITE;
/*!40000 ALTER TABLE `cheques` DISABLE KEYS */;
INSERT INTO `cheques` VALUES (1,'12345123451234512345123451234512345123451234512345',123.00,'cerecerecerecerecerecerecerecerecerecereerecerecerecerecerecere','0000-00-00','COMPENSADO','2026-03-28 01:13:40',0),(2,'123456789010',1239.98,'cliente joao lucas','2028-10-30','PENDENTE','2026-03-30 19:06:56',1),(3,'123123123123123',23.00,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','0000-00-00','PENDENTE','2026-03-30 23:20:33',1);
/*!40000 ALTER TABLE `cheques` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) NOT NULL,
  `cpf_cnpj` varchar(20) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `endereco` varchar(200) DEFAULT NULL,
  `observacoes` text DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT 1,
  `criado_em` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'eba','','','','',0,'2026-03-27 20:39:48'),(2,'asdasd','31.431.333/3333-33','(34) 32','','',0,'2026-03-27 23:07:48'),(3,'suca','','','','',0,'2026-03-29 18:32:43'),(4,'super maria rosa da silva da zauro da trip jeans','123.123.123-21','(22) 22222-2222','rua 12 de agfrgwr werghadsgrua 12 de agfrgwr werghadsg','nenhuyma',0,'2026-03-29 18:34:47'),(5,'clioente42','12.312.312/3123-12','(23) 33333-3333','rua 2','',0,'2026-03-29 18:34:57'),(6,'cliowmte','','','','',0,'2026-03-29 18:35:02'),(7,'setimo','','','carasdasd','ca',0,'2026-03-29 23:54:10'),(8,'oitavo','','','','',0,'2026-03-29 23:54:13'),(9,'nono','','','','',0,'2026-03-29 23:54:31'),(10,'dez','','','caceteacaceteacaceteacaceteacaceteacaceteacaceteacaceteacaceteacaceteacaceteacacetea','',0,'2026-03-29 23:54:37'),(11,'onzce','','','','',0,'2026-03-29 23:54:40'),(12,'doze','','','','',0,'2026-03-29 23:54:43'),(13,'Teste1 Super Clientententententente','00.000.000/0000-00','(11) 11111-1111','Rua numero cidaade testeRua numero cidaade testeRua numero cidaade testeRua numero cidaade teste','obs obs obs obs obs obs obs obsobs obs obs obs obs obs obs obsobs obs obs obs obs obs obs obs',1,'2026-03-30 19:05:14'),(14,'cliente 2','123.123.123-22','','eeeeeeeeeeeeeeeeeeeeeee','',1,'2026-03-30 20:44:19');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lojas`
--

DROP TABLE IF EXISTS `lojas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lojas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `contato` varchar(120) DEFAULT NULL,
  `shopping_id` int(11) DEFAULT NULL,
  `observacoes` text DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT 1,
  `criado_em` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `shopping_id` (`shopping_id`),
  CONSTRAINT `lojas_ibfk_1` FOREIGN KEY (`shopping_id`) REFERENCES `shopping` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lojas`
--

LOCK TABLES `lojas` WRITE;
/*!40000 ALTER TABLE `lojas` DISABLE KEYS */;
INSERT INTO `lojas` VALUES (1,'loja1 de asdloja1 de','(12) 33333-3333',NULL,'',0,'2026-03-27 20:56:47'),(2,'loja2 de asd','(21) 33333-3333',NULL,'eeeeeeeeeeeeeeeee',0,'2026-03-29 18:33:44'),(3,'loja egeag','(33) 33333-3333',NULL,'oooooooooooooooooooooooooooooooooooooo',0,'2026-03-29 18:34:09'),(4,'loka shopp4','(12) 31231-2312',NULL,'123123123123123',0,'2026-03-29 18:34:19'),(5,'lojka testa','(22) 22222-2222',NULL,'',0,'2026-03-29 18:34:27'),(6,'super loja teste','(51) 99999-9999',5,'0opooooooooooooooo0opooo0opooooooooooooooo0opooooooooooooooooooooooooooo',1,'2026-03-30 19:05:49'),(7,'çlloja2','',6,'',1,'2026-03-30 20:54:17'),(8,'LOJA2','(22) 22222-2222',6,'',1,'2026-03-30 20:55:36');
/*!40000 ALTER TABLE `lojas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `viagem_id` int(11) NOT NULL,
  `loja_id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `tipo` varchar(255) DEFAULT NULL,
  `ordem` int(11) DEFAULT NULL,
  `observacoes` text DEFAULT NULL,
  `status` enum('Pendente','Visitado','Concluido','Cancelado') DEFAULT 'Pendente',
  `criado_em` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `viagem_id` (`viagem_id`),
  KEY `loja_id` (`loja_id`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`viagem_id`) REFERENCES `viagens` (`id`),
  CONSTRAINT `pedidos_ibfk_3` FOREIGN KEY (`loja_id`) REFERENCES `lojas` (`id`),
  CONSTRAINT `pedidos_ibfk_4` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (38,7,8,14,'PEDIDO,ACERTO,TROCA,DEFEITO,DEVOLUCAO',1,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','Pendente','2026-03-30 22:42:31'),(39,7,6,13,'PEDIDO,DEFEITO,DEVOLUCAO',1,'','Pendente','2026-03-30 23:05:26'),(40,7,7,13,'PEDIDO,ACERTO',1,'','Pendente','2026-03-30 23:05:33');
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shopping`
--

DROP TABLE IF EXISTS `shopping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shopping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `local` varchar(50) DEFAULT NULL,
  `endereco` varchar(200) DEFAULT NULL,
  `contato` varchar(120) DEFAULT NULL,
  `observacoes` text DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT 1,
  `criado_em` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shopping`
--

LOCK TABLES `shopping` WRITE;
/*!40000 ALTER TABLE `shopping` DISABLE KEYS */;
INSERT INTO `shopping` VALUES (1,'egeag','Serra','','','',0,'2026-03-27 20:56:42'),(2,'testa','Santa Catarina','','','',0,'2026-03-27 21:18:31'),(3,'asd','Serra','','(11) 11111-1111','',0,'2026-03-27 21:58:22'),(4,'shop 4shop 4shop','Santa Catarina','rua 32 de 3f1frua 32 de 3f1frua 32 de 3f1frua 32 de 3f1frua 32 de 3f1f','(23) 11111-1111','',0,'2026-03-29 18:33:25'),(5,'Iguatemi e coisarada','Serra','rua numero nao sei oq e darua numero nao sei oq e da','(51) 99999-9999','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',1,'2026-03-30 19:05:37'),(6,'shopp2','Santa Catarina','','','',1,'2026-03-30 20:54:08');
/*!40000 ALTER TABLE `shopping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `viagem_clientes`
--

DROP TABLE IF EXISTS `viagem_clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `viagem_clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `viagem_id` int(11) DEFAULT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `ordem` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `viagem_clientes`
--

LOCK TABLES `viagem_clientes` WRITE;
/*!40000 ALTER TABLE `viagem_clientes` DISABLE KEYS */;
INSERT INTO `viagem_clientes` VALUES (24,7,13,2),(25,7,14,1);
/*!40000 ALTER TABLE `viagem_clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `viagem_financeiro`
--

DROP TABLE IF EXISTS `viagem_financeiro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `viagem_financeiro` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `viagem_id` int(11) NOT NULL,
  `tipo` enum('CUSTO','GANHO') NOT NULL,
  `valor` decimal(10,2) NOT NULL,
  `descricao` varchar(200) DEFAULT NULL,
  `criado_em` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `viagem_id` (`viagem_id`),
  CONSTRAINT `viagem_financeiro_ibfk_1` FOREIGN KEY (`viagem_id`) REFERENCES `viagens` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `viagem_financeiro`
--

LOCK TABLES `viagem_financeiro` WRITE;
/*!40000 ALTER TABLE `viagem_financeiro` DISABLE KEYS */;
INSERT INTO `viagem_financeiro` VALUES (3,7,'CUSTO',100.00,'','2026-03-30 22:41:47'),(4,7,'GANHO',233.00,'suuuuuuuuuuuuuuuuuuuuuuuuuuuuu','2026-03-30 22:41:54'),(6,7,'GANHO',12.00,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','2026-03-30 22:43:35');
/*!40000 ALTER TABLE `viagem_financeiro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `viagem_loja`
--

DROP TABLE IF EXISTS `viagem_loja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `viagem_loja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `viagem_id` int(11) NOT NULL,
  `shopping_id` int(11) NOT NULL,
  `loja_id` int(11) NOT NULL,
  `ordem` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `viagem_loja`
--

LOCK TABLES `viagem_loja` WRITE;
/*!40000 ALTER TABLE `viagem_loja` DISABLE KEYS */;
INSERT INTO `viagem_loja` VALUES (1,6,3,1,1),(2,6,2,5,1),(3,6,1,3,1),(4,6,4,4,1),(5,6,3,2,2),(6,7,5,6,1),(7,7,6,7,2),(8,7,6,8,1);
/*!40000 ALTER TABLE `viagem_loja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `viagem_shopping`
--

DROP TABLE IF EXISTS `viagem_shopping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `viagem_shopping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `viagem_id` int(11) NOT NULL,
  `shopping_id` int(11) NOT NULL,
  `ordem` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_vs_viagem` (`viagem_id`),
  KEY `fk_vs_shopping` (`shopping_id`),
  CONSTRAINT `fk_vs_shopping` FOREIGN KEY (`shopping_id`) REFERENCES `shopping` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_vs_viagem` FOREIGN KEY (`viagem_id`) REFERENCES `viagens` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `viagem_shopping`
--

LOCK TABLES `viagem_shopping` WRITE;
/*!40000 ALTER TABLE `viagem_shopping` DISABLE KEYS */;
INSERT INTO `viagem_shopping` VALUES (1,6,3,1),(2,6,2,2),(3,6,1,4),(4,6,4,3),(5,7,5,1),(6,7,6,2);
/*!40000 ALTER TABLE `viagem_shopping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `viagens`
--

DROP TABLE IF EXISTS `viagens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `viagens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_viagem` date DEFAULT NULL,
  `observacoes` text DEFAULT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'Planejada',
  `ativo` tinyint(1) DEFAULT 1,
  `criado_em` timestamp NOT NULL DEFAULT current_timestamp(),
  `local` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `viagens`
--

LOCK TABLES `viagens` WRITE;
/*!40000 ALTER TABLE `viagens` DISABLE KEYS */;
INSERT INTO `viagens` VALUES (1,'2023-03-12','','Planejada',0,'2026-03-27 20:26:40','Serra'),(2,'2023-03-12','','Planejada',0,'2026-03-27 20:26:46','Santa Catarina'),(3,'2025-03-12','','Planejada',0,'2026-03-27 20:26:54','Santa Catarina'),(4,'2030-03-12','','Planejada',0,'2026-03-27 20:27:03','Santa Catarina'),(5,'2024-03-12','','Planejada',0,'2026-03-27 20:27:12','Serra'),(6,'2030-03-12','','Planejada',0,'2026-03-27 20:53:49','Serra'),(7,'2029-11-29','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','Planejada',1,'2026-03-30 19:06:13','Serra'),(8,'2029-11-25','','Planejada',1,'2026-03-30 23:13:06','Serra');
/*!40000 ALTER TABLE `viagens` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-31  1:44:07
