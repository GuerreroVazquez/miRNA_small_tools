import pytest
import numpy as np
import paper_helper.resources.datasets_values as dv
from paper_helper import column_divider



def test_getting_file():
    """
    This test will evaluate the capacity of the column divider to get the files

    :return:
    """
    for database in dv.DatasetValues:
        column_divider.get_data_from_databse(database)
    assert True
