--
-- Table structure for table `mirna_target`
-- is the relational table between the mirna form mirBase and the mRNA targets
-- from the other datasets
-- mrna: The mRNA where the miRNA bins
-- mirna_id: The current id in miRBase
-- auto_binging: the unique id from the binding table
-- probability: the probability of that miRNA binds with that mRNA
-- source: Database where I got the information from
--  tmpmirna: The mirna id (to be removed after the creation of the tables)
--  tmpprobability: The probability of that particular binding
DROP TABLE IF EXISTS `mirna_target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
Create table `mirna_target` (
 `mirna_id` text NOT NULL,
 `auto_binding` text NOT NULL DEFAULT '',
 `probability` float NOT NULL DEFAULT '0',
 `source` text NOT NULL DEFAULT 'mirwalk',
 --INDEX par_ind (mirna_id),
 --FOREIGN KEY (mirna_id)
 --       REFERENCES mirna(mirna_id)
 --       ON DELETE CASCADE
 )

