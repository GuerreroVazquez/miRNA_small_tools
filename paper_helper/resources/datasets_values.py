# This file takes care of the information of the databases
from enum import Enum


class DatasetValues(Enum):
    mirWalk = 'mirWalk'
    miRDB = 'miRDB'
    hmdd = 'HMDD'
    mirTarBase = 'mirTarBase'
    DianaTed = 'diana_miTed'

    def describe(self):
        # self is the member here
        return self.name, self.value

    def get_sep(self):
        """
        To make this compatible to future datasets, this will define the type of separation of the file
        normaly it will br '\t' or ','
        :return:
        """
        sep = {'mirWalk': '\t',
               'miRDB': '\t',
               'HMDD': '\t',
               'mirTarBase': '\t',
               'diana_miTed': '\t'}
        return sep[self.value]

    def get_columns(self):
        columns = {'mirWalk': ["miRNA", "mRNA", "Genesymbol", "binding_site", "duplex", "binding_probability"],
                   'miRDB': ["miRNA", "mRNA", "Prediction probability percentage"],
                   'HMDD': ["category", "mir", "disease", "pmid", "description"],
                   'mirTarBase': ["miRTarBase_ID", "miRNA", "Species", "Target_Gene", "Target_Gene_ID", "Species2",
                                  "Target_Site", "Experiments_Support Type", "References"],
                   'diana_miTed': ["S.No", "Sample_ID", "Collection", "Project_ID", "Tissue_or_organ_of_origin",
                                "Tissue_subregion", "Cell_Line", "Disease", "Organism", "Gender", "Health_state",
                                "Tissue_definition", "ALL MIRNAS (2464)"]
                   }
        return columns[self.value]

    def get_consensus_column_name(self, column):
        """
        This function is a manual curation of the columns in order to have a
        similar column name and compatible tables.
        :param column: The column name that we are looking for
        :return: list str: list of possible options to look for
        """
        names = {'mrna': ["mRNA", "Target_Gene"],
                 'mirna_id': ["miRNA", "mir"],
                 'binding_site': ["binding_site"],
                 'sequence': ["duplex", "Target_Site"],
                 'species': ['miRNA', 'Organism', 'Species'],
                 'tmpmirna': ["miRNA", "mir"],
                 'tmpprobability': ['binding_probability', 'Prediction probability percentage'],
                 'source': []
                 }
        return names[column]

    def get_file(self):
        """
        Returns the name of the files that cointains information.
        Some datasets will cointain just one, other multiple, different formats, etc

        :return:
        """
        file_name = {
            'mirWalk': ['dre_miRWalk_3UTR.txt', 'hsa_miRWalk_5UTR.txt', 'mmu_miRWalk_3UTR.txt', 'mmu_miRWalk_5UTR.txt'],
            'miRDB': ['miRDB_v6.0_prediction_result.txt'],
            'diana_miTed': ["miTED-ALL_read_counts.tsv", "miTED-ALL_rpm.tsv", "miTED-Log2RPM.tsv"],
            'HMDD': ["target.txt", "tissue_expression.txt"],
            'mirTarBase': ["miRTarBase_Target.txt"]
        }
        return file_name[self.value]
