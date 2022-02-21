###
# This file will contain the classes to distinguish the different columns of the
# databases. For this I will annotate them on a header(?) maybe, maybe a dictionary
# with the equivalences
###
import resources.datasets_values as dv
import pandas as pd
from paper_helper.resources.file_adress import DatabasesDataset as paths
from sql_metadata import Parser


def get_binding_columns():
    """
    This function will go thH91 F9K3ough the databases and will collect the information (if cointaned)
    and renamed the columns as needed.
    :return:
    """


def get_data_from_databse(database_name: dv.DatasetValues):
    """
    This function will get the file and load the data in a dataframe
    :param database_name: The name of the
    :return:
    """
    files = database_name.get_file()

    columns = database_name.get_columns()
    for file in files:
        df = get_dataframe_from_file(database_name=database_name, file=file, first_column=columns[0])
        df.columns = database_name.get_columns()
        binding_columns = ['mrna', 'binding_site', 'sequence', 'source', 'tmpmirna',
                           'tmpprobability']
        new_df = pd.DataFrame([], columns=binding_columns)
        for bc in binding_columns:
            equivalent_columns = database_name.get_consensus_column_name(bc)
            for column in equivalent_columns:
                if column in df.columns:
                    new_df[bc] = df[column]
        new_df['source']=database_name.value
        pass

    pass


def get_dataframe_from_file(database_name: str, file: str, first_column: str):
    sep = database_name.get_sep()
    full_path = paths.datasets_folder.get() + database_name.value + "/" + file
    with open(full_path, 'r') as f:
        first_value = f.readline().split(sep)[0]
        if first_value == first_column[0]:
            header = 0
        else:
            header = None

    df = pd.read_csv(full_path, sep=sep, header=header)
    return df
