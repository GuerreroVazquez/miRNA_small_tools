###
# This file will contain the classes to distinguish the different columns of the
# databases. For this I will annotate them on a header(?) maybe, maybe a dictionary
# with the equivalences
###
from resources import datasets_values as dv
import pandas as pd
from resources.file_adress import DatabasesDataset as paths


def get_binding_columns():
    """
    This function will go through the databases and will collect the information (if contained)
    and renamed the columns as needed.
    :return:
    """
    return ['mrna', 'binding_site', 'sequence', 'source', 'tmpmirna',
            'tmpprobability']


def process_all_files(database_name: dv.DatasetValues):
    """
    This function will process all the files of a given database
    :param database_name:
    :return:
    """
    files = database_name.get_file()

    for file in files:
        df = get_data_from_database(file=file, database_name=database_name)
        save_dataframe_in_file(data=df, file_name=database_name.value + "_" + file)


def get_data_from_database(file: str, database_name: dv.DatasetValues):
    """
    This function will get the file and load the data in a dataframe
    :param file: The file where we are going to get the data.
    :param database_name: The name of the
    :return:
    """
    columns = database_name.get_columns()
    df = get_dataframe_from_file(database_name=database_name, file=file, first_column=columns[0])
    columns = database_name.get_columns()
    if len(columns) < len(df.columns):
        df.drop(df.columns[len(columns):len(df.columns)], axis=1, inplace=True)
    df.columns = columns
    binding_columns = get_binding_columns()
    new_df = pd.DataFrame([], columns=binding_columns)
    for bc in binding_columns:
        equivalent_columns = database_name.get_consensus_column_name(bc)
        for column in equivalent_columns:
            if column in df.columns:
                new_df[bc] = df[column]
    new_df['source'] = database_name.value

    return new_df


def save_dataframe_in_file(file_name: str, data):
    """

    :param file_name:
    :param data:
    :return:
    """
    full_path = paths.datasets_folder.get() + "parsed/" + file_name
    data.to_csv(full_path, sep="\t", index=False, header=False)


def get_dataframe_from_file(database_name: str, file: str, first_column: str):
    sep = database_name.get_sep()
    full_path = paths.datasets_folder.get() + database_name.value + "/" + file
    with open(full_path, 'r') as f:
        first_value = f.readline().split(sep)[0]
        if first_value == first_column:
            header = 0
        else:
            header = None

    df = pd.read_csv(full_path, sep=sep, header=header)
    return df


def main():
    """

    :return:
    """
    target_databases = [dv.DatasetValues.mirTarBase, dv.DatasetValues.mirWalk, dv.DatasetValues.miRDB]
    target_databases = [dv.DatasetValues.miRDB]
    target_databases = [dv.DatasetValues.targetScan]
    for database in target_databases:
        process_all_files(database)


if __name__ == "__main__":
    main()
