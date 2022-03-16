use mirnadbs;
LOAD DATA LOCAL INFILE 'confidence_score.txt' INTO TABLE confidence_score ;
LOAD DATA LOCAL INFILE 'dead_mirna.txt' INTO TABLE dead_mirna ;
LOAD DATA LOCAL INFILE 'literature_references.txt' INTO TABLE literature_references ;
LOAD DATA LOCAL INFILE 'mature.txt' INTO TABLE mature ;
LOAD DATA LOCAL INFILE 'mature_database_links.txt' INTO TABLE mature_database_links ;
LOAD DATA LOCAL INFILE 'mature_database_url.txt' INTO TABLE mature_database_url ;
LOAD DATA LOCAL INFILE 'mirna.txt' INTO TABLE mirna ;
LOAD DATA LOCAL INFILE 'mirna_2_prefam.txt' INTO TABLE mirna_2_prefam ;
LOAD DATA LOCAL INFILE 'mirna_chromosome_build.txt' INTO TABLE mirna_chromosome_build ;
LOAD DATA LOCAL INFILE 'mirna_context.txt' INTO TABLE mirna_context ;
LOAD DATA LOCAL INFILE 'mirna_database_links.txt' INTO TABLE mirna_database_links ;
LOAD DATA LOCAL INFILE 'mirna_database_url.txt' INTO TABLE mirna_database_url ;
LOAD DATA LOCAL INFILE 'mirna_literature_references.txt' INTO TABLE mirna_literature_references ;
LOAD DATA LOCAL INFILE 'mirna_mature.txt' INTO TABLE mirna_mature ;
LOAD DATA LOCAL INFILE 'mirna_pre_mature.txt' INTO TABLE mirna_pre_mature ;
LOAD DATA LOCAL INFILE 'mirna_prefam.txt' INTO TABLE mirna_prefam ;
LOAD DATA LOCAL INFILE 'mirna_species.txt' INTO TABLE mirna_species ;
LOAD DATA LOCAL INFILE 'organisms.txt' INTO TABLE organisms ;
