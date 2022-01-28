####This class will help with the analysis of articles reading in order to avoid manual searchs
#
import requests
from bs4 import BeautifulSoup

from paper_helper.common_tools import get_csv_into_dictionary


class EvaluatePapers:
    def __init__(self, url_address="https://pubmed.ncbi.nlm.nih.gov/", pubmed_ids=[]):
        self.url = url_address
        self.pubmed_ids = pubmed_ids
        self.categories = self.get_all_categories()

    def get_number_cites(self, article_id):
        """
        This function should take the pubmed number and give the exact a
        :return: int
        """
        url = self.url + article_id
        soup = self.get_soup_from_html(url)
        soup = self.find_section_class_type(soup=soup, object_type="em", class_name="amount")
        if soup:
            amount = self.get_soup_text(soup)
            amount = amount.replace(",", "")
        else:
            amount = 0
        return int(amount)

    def get_number_cites_from_list(self, article_ids):
        cites = []
        for article_id in article_ids:
            cites.append(self.get_number_cites(article_id))
        return cites


    def get_soup_from_html(self, url):
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        return soup

    def find_all_section_class_type(self, soup=None, object_type="div", class_name="citedby-articles"):
        """
        This function will find all the object with that class name
        :param soup:
        :param object_type:
        :param class_name:
        :return:
        """
        if not soup:
            soup = self.soup
        result_soups = soup.find_all(object_type, {"class": class_name})
        return result_soups

    def find_section_class_type(self, soup=None, object_type="div", class_name="citedby-articles"):
        """
        This function gets the first (maybe only) ocurrence of the object - class combination
        :param soup:
        :param object_type:
        :param class_name:
        :return:
        """
        if not soup:
            soup = self.soup
        result_soup = soup.find(object_type, {"class": class_name})
        return result_soup

    def __str__(self):
        return self.soup.text

    def get_soup_text(self, soup):
        return soup.text

    def get_html(self):
        return self.soup.prettify()

    def get_paper_data_from_file(self, file_name="paper_helper/resources/data/papers_data.csv"):
        paper_data = get_csv_into_dictionary(file_name=file_name)
        for paper in paper_data:
            paper["cite_number"] = self.get_number_cites(paper["PubmedID"])
        return paper_data

    def get_categores(self):

        pass

    def get_all_categories(self):

        pass




