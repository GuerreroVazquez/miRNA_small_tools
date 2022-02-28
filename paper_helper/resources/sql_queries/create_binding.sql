use mirnadbs;

--
-- Table structure for table `binding`
-- modified version of mirwalk and compatible with miRtarbase
-- auto_binding: New column to identify the binding
-- mrna: The mRNA where the miRNA bins
-- gene_target: (Gene symbol) of the gene that is being target
-- mirna: The mirbase name WITHOUT -5p ending or stuff
-- binding_site: The coordinates of the binding start,finish
-- sequence: The actual secuence of the binding
-- suffix: the -5 -3 stuff
-- species: The origin spices of the miRNA
-- source: Database where I got the information from
--  tmpmirna: The mirna id (to be removed after the creation of the tables)
--  tmpprobability: The probability of that particular binding
DROP TABLE IF EXISTS `binding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
Create table `binding` (
 `auto_binding` int(10) NOT NULL AUTO_INCREMENT,
 `mrna` text,
 `binding_site` text,
 `sequence` text,
 `source` text NOT NULL DEFAULT 'mirwalk',
 `tmpmirna` text NOT NULL,
 `tmpprobability` float NOT NULL DEFAULT '0',
 PRIMARY KEY (`auto_binding`),
 )ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
