import csv
import bios
import requests
from bs4 import BeautifulSoup


def get_list_from_file(file_name="resources/data/human_only_databases_list.txt"):
    with open(file_name, 'r') as file:
        file = file.read()
        file_list = file.split("\n")
    return file_list


def get_csv_into_dictionary(file_name="resources/data/human_only_databases_list.txt"):
    with open(file_name, 'r') as f:
        dic = [{k: str(v) for k, v in row.items()}
               for row in csv.DictReader(f, skipinitialspace=True)]
    return dic


def write_dictionary_to_csv(file_name="x.csv", dic=None):
    if dic is None:
        dic = {}
    with open(file_name, mode='w') as outfile:
        writer = csv.writer(outfile)
        mydict = {rows[0]: rows[1] for rows in dic}


def yml_to_dict(
        file_name=r"C:\Users\crtuser\Documents\PhD\Project\repos\miRNA_small_tools\paper_helper\resources\data\db_categories.yml"):
    my_dict = bios.read(file_name)
    return my_dict


def get_soup_from_html(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup
