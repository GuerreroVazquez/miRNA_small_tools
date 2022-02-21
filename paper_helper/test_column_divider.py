import pytest
import numpy as np
import paper_helper.resources.datasets_values as dv
from paper_helper import column_divider
from paper_helper.resources.file_adress import DatabasesDataset


def test_getting_file(monkeypatch):
    """
    This test will evaluate the capacity of the column divider to get the files

    :return:
    """
    def fake_folder(*args, **kwargs):
        fake = DatabasesDataset.datasets_folder
        fake_str = fake.value + 'mini_test/'
        return fake_str
    monkeypatch.setattr("paper_helper.resources.file_adress.DatabasesDataset.get",fake_folder)
    for database in dv.DatasetValues:
        column_divider.get_data_from_databse(database)
    assert True
