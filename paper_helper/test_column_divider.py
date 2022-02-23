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

    monkeypatch.setattr("paper_helper.resources.file_adress.DatabasesDataset.get", fake_folder)
    file = "dre_miRWalk_3UTR.txt"
    database = dv.DatasetValues.mirWalk
    df = column_divider.get_data_from_database(file=file, database_name=database)
    first_row = df.iloc[0].tolist()
    assert first_row[0] == 'NM_001001398', "The first value is not ok"
    assert True

def test_process_all_files_for_diana(monkeypatch):
    def fake_folder(*args, **kwargs):
        fake = DatabasesDataset.datasets_folder
        fake_str = fake.value + 'mini_test/'
        return fake_str
    monkeypatch.setattr("paper_helper.resources.file_adress.DatabasesDataset.get", fake_folder)
    database = dv.DatasetValues.DianaTed
    column_divider.process_all_files(database)
    assert True

def test_process_all_files_for_miRTarBase(monkeypatch):
    def fake_folder(*args, **kwargs):
        fake = DatabasesDataset.datasets_folder
        fake_str = fake.value + 'mini_test/'
        return fake_str
    monkeypatch.setattr("paper_helper.resources.file_adress.DatabasesDataset.get", fake_folder)
    database = dv.DatasetValues.mirTarBase
    column_divider.process_all_files(database)
    assert True

def test_process_all_files(monkeypatch):
    def fake_folder(*args, **kwargs):
        fake = DatabasesDataset.datasets_folder
        fake_str = fake.value + 'mini_test/'
        return fake_str

    monkeypatch.setattr("paper_helper.resources.file_adress.DatabasesDataset.get", fake_folder)
    for database in dv.DatasetValues:
        column_divider.process_all_files(database)
    assert True
