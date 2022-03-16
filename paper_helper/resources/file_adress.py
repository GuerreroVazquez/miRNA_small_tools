from enum import Enum


class DatabasesDataset(Enum):
    resources = "/resources/data/"
    chapter7 = "papers_data.csv"
    all_mirna = "pubmed_results_mirna.csv"  # ("microRNA" or "miRNA") and
    # ("database" or "repository" or "dataset")
    mirna_database = "pubmed_results_databses.csv"  # ("database"[Title] OR "repository"[Title] OR
    # "dataset"[Title]) AND ("miRNA"[Title] OR "microRNA"[Title] OR "micro RNA"[Title])
    database_categories = "db_categories.yml"
    pareto_front_merge = "pareto_fronts_databases/merge.csv"  # The merge of the 3
    # pareto fronts generated for chapter7, all_mirna and  mirna_database
    # datasets_folder = "/home/karen/Documents/phd/year1/Databases/"
    datasets_folder = "/media/karen/A0000B91000B6E1A/Users/crtuser/Documents/PhD/Project/Databases/"

    def get(self):
        return self.value
