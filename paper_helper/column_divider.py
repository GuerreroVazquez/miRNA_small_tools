###
# This file will contain the classes to distinguish the different columns of the
# databases. For this I will annotate them on a header(?) maybe, maybe a dictionary
# with the equivalences
###
import resources.datasets_values as dv
import pandas as pd


def get_binding_columns():
    """
    This function will go thH91 F9K3ough the databases and will collect the information (if cointaned)
    and renamed the columns as needed.
    :return:
    """

def get_data_from_databse(datbase_name:dv.DatasetValues):
    """
    This function will get the file and load the data in a dataframe
    :param datbase_name: The name of the
    :return:
    """
    files = datbase_name.get_file()
    sep = 
    for file in files:
        df = pd.read_csv(file, sep=sep, header=header)
    pass






