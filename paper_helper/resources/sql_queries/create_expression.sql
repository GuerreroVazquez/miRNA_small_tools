-- This table will store the levels of expression of a miRNA
--
DROP TABLE IF EXISTS `expression`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
Create table `expression` (
 `auto_expression` int(10) NOT NULL AUTO_INCREMENT,
 `sequence` text NOT NULL DEFAULT '',
 `sufix` text,
 `species` bigint,
 `source` text NOT NULL DEFAULT 'mirwalk',
 `tmpmirna` text NOT NULL,
 `tmpprobability` float NOT NULL DEFAULT '0',
 PRIMARY KEY (`auto_prefam`),
 )
