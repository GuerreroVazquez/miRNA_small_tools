from bs4 import BeautifulSoup

from paper_helper import common_tools
from paper_helper.common_tools import get_list_from_file, yml_to_dict
from paper_screener.paper_helper import RecollectPapers

helper = RecollectPapers()
short_csv = [{'database': 'Antagomirbase', 'year': '2011', 'Organism': 'Unspecified',
              'Website': 'http://bioinfopresidencycollegekolkata.edu.in/antagomirs.html', 'Download': 'No',
              'Available': 'No',
              'PubmedID': '21904438'},
             {'database': 'ARN', 'year': '2016', 'Organism': 'Unspecified', 'Website': 'http://210.27.80.93/arn/',
              'Download': 'No', 'Available': 'Yes', 'PubmedID': '27503118'}]


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
    monkeypatch.setattr(common_tools, "get_soup_from_html", lambda *args, **kwargs: html)
    papers_ids = ["21904438", "14681370"]
    helper.pubmed_ids = papers_ids
    cites = helper.get_number_cites_from_list(papers_ids)
    assert cites[0] >= 2, "in january 2022 it was 2, so there could not be less than that"
    assert cites[1] >= 910, "in january 2022 it was 910, so there could not be less than that"


def test_get_list_from_file():
    databases = get_list_from_file(file_name="../../resources/data/human_only_databases_list.txt")
    assert isinstance(databases, list)


def test_get_paper_data(monkeypatch):
    """
    This test will make sure to have all the 8 fields of the datasets;
    'database', 'year', 'Organism', 'Website', 'Download', 'Available', 'PubmedID', and 'cite_number'
    :param monkeypatch:
    :return:
    """
    helper.category_list_address = "../../paper_helper/resources/data/db_categories.yml"

    monkeypatch.setattr(common_tools, "get_csv_into_dictionary", lambda *args, **kwargs: short_csv)
    dics = helper.get_paper_data_from_file(file_name="../test_resources/papers_data.csv")
    assert isinstance(dics, list)
    dic = dics[0]
    assert len(dic) == 8


def test_get_yml_from_file():
    dic = yml_to_dict(file_name="../../resources/data/db_categories.yml")
    assert isinstance(dic, dict)
    assert dic['Regulation network']


def test_categories():
    helper.category_list_address = r"../../resources/data/db_categories.yml"
    category_list = helper.get_categories("microPIR")
    assert isinstance(category_list, list)
    assert 'miRNA - target -' in category_list[0]
    pass


def test_get_information():
    helper.information_list_address = r"../../resources/data/db_information.yml"
    information_list = helper.get_information("mirbase")
    assert isinstance(information_list, list)
    assert 'miRNA/Target interactions - ' in information_list


def test_write_list_of_dict():
    helper.write_list_of_dict(short_csv)


def test_merge_article_files_by():
    helper.merge_article_files_by(files_2_merge=["../../resources/data/pareto_fronts_databases/papers_data.csv",
                                                 "../../resources/data/pareto_fronts_databases/pubmed_results_databses.csv",
                                                 "../../resources/data/pareto_fronts_databases/pubmed_results_mirna.csv"])
    pass
