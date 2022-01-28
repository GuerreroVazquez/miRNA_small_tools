import pytest
import requests

from bs4 import BeautifulSoup

from paper_helper import common_tools
from paper_helper.common_tools import get_list_from_file, yml_to_dict, get_csv_into_dictionary
from paper_helper.paper_helper import EvaluatePapers

helper = EvaluatePapers()


def test_find_amount():
    with open("../test_resources/ncbi_found_article.html", 'r') as file:
        html = file.read()
        html = BeautifulSoup(html, "html.parser")
    soup = helper.find_section_class_type(soup=html, object_type="em", class_name="amount")
    amount = helper.get_soup_text(soup)
    assert int(amount) == 128


def test_get_number_of_cites(monkeypatch):
    with open("../test_resources/ncbi_found_article.html", 'r') as file:
        html = file.read()
        html = BeautifulSoup(html, "html.parser")
    monkeypatch.setattr(EvaluatePapers, "get_soup_from_html", lambda *args, **kwargs: html)
    papers_ids = ["21904438", "14681370"]
    helper.pubmed_ids = papers_ids
    cites = helper.get_number_cites_from_list(papers_ids)
    assert cites == [128, 128]


def test_get_list_from_file():
    databases = get_list_from_file(file_name="../../paper_helper/resources/data/human_only_databases_list.txt")
    assert isinstance(databases, list)


def test_get_paper_data(monkeypatch):
    short_csv = [{'database': 'Antagomirbase', 'year': '2011', 'Organism': 'Unspecified',
                  'Website': 'http://bioinfopresidencycollegekolkata.edu.in/antagomirs.html', 'Download': 'No',
                  'Available': 'No',
                  'PubmedID': '21904438'},
                 {'database': 'ARN', 'year': '2016', 'Organism': 'Unspecified', 'Website': 'http://210.27.80.93/arn/',
                  'Download': 'No', 'Available': 'Yes', 'PubmedID': '27503118'}]
    monkeypatch.setattr(common_tools, "get_csv_into_dictionary", lambda *args, **kwargs: short_csv)
    dic = helper.get_paper_data_from_file(file_name="../test_resources/papers_data.csv")
    assert isinstance(dic, dict)
    assert len(dic) == 2


def test_get_yml_from_file():
    dic = yml_to_dict(file_name="../../paper_helper/resources/data/db_categories.yml")
    assert True
