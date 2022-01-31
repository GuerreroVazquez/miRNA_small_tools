####This class will help with the analysis of articles reading in order to avoid manual searchs
#
import requests
from bs4 import BeautifulSoup
import numpy as np
from paper_helper.common_tools import get_csv_into_dictionary, yml_to_dict, get_soup_from_html


class RecollectPapers:
    def __init__(self, url_address="https://pubmed.ncbi.nlm.nih.gov/", pubmed_ids=[]):
        self.url = url_address
        self.pubmed_ids = pubmed_ids
        self.category_list_address = "paper_helper/resources/data/db_categories.yml"

    def get_number_cites(self, article_id):
        """
        This function should take the pubmed number and give the exact a
        :return: int
        """
        url = self.url + article_id
        soup = get_soup_from_html(url)
        soup = self.find_section_class_type(soup=soup, object_type="em", class_name="amount")
        if soup:
            amount = self.get_soup_text(soup)
            amount = amount.replace(",", "")
        else:
            amount = 0
        return int(amount)

    def get_number_cites_from_list(self, article_ids):
        """
        When given a list of ids, this will look fot he ids of all elements on the list
        :param article_ids: str list
        :return: str list  the number of cites that those articles have
        """
        cites = []
        for article_id in article_ids:
            cites.append(self.get_number_cites(article_id))
        return cites

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

    def get_paper_data_from_file(self, file_name="paper_helper/resources/data/papers_data.csv",
                                 paper_data=None):
        if not paper_data:
            paper_data = get_csv_into_dictionary(file_name=file_name)
        for paper in paper_data:
            paper["cite_number"] = self.get_number_cites(paper["PubmedID"])
            paper["categories"] = self.get_categories(database_name=paper["database"])
        return paper_data

    def get_categories(self, database_name=""):
        """
        Get the categories from the category list (YML) and find all
         the categories that a particular ddtabase is in
        :param database_name:
        :return: str list the categories
        """
        categories = yml_to_dict(self.category_list_address)
        database_name = database_name.lower()
        category_list = []
        for category in categories.keys():
            if database_name in categories[category].lower():
                category_list.append(category)
        return category_list

    def get_all_categories(self, file_name="paper_helper/resources/data/papers_data.csv",
                           paper_data=None):
        if not paper_data:
            paper_data = self.get_paper_data_from_file(file_name)
        for database in paper_data:
            database["categories"] = self.get_categories(database_name=paper_data["database"])
        return paper_data

    def collect_data(self, papers_file="paper_helper/resources/data/papers_data.csv"):
        paper = self.get_paper_data_from_file(papers_file)
        paper = self.get_all_categories(paper_data=paper)


class EvaluatePapers:
    def __init__(self, papers_info):
        self.papers_info = papers_info

    def get_pareto_cites_year(self, plot=False):
        """
        This function will retrieve the pareto set of the
        max year
        max cites
        :param plot: If we should plot the pareto
        :return:
        """
        cite_years = []
        for paper in self.papers_info:
            cite_years.append([-int(paper["year"]), -int(paper["cite_number"])])
        npArray = np.array(cite_years)
        pareto = self.is_pareto_efficient(npArray)
        pareto_bool = pareto.tolist()
        pareto_values = []
        for count, paper in enumerate(self.papers_info):
            if pareto_bool[count]:
                pareto_values.append(paper)
        if plot:
            self.plot_pareto(npArray, pareto)
        return pareto_values

    def is_pareto_efficient(self, costs, return_mask=True):
        """
        Find the pareto-efficient points
        Obtainded from https://github.com/QUVA-Lab/artemis/blob/peter/artemis/general/pareto_efficiency.py
        :param costs: An (n_points, n_costs) array
        :param return_mask: True to return a mask
        :return: An array of indices of pareto-efficient points.
            If return_mask is True, this will be an (n_points, ) boolean array
            Otherwise it will be a (n_efficient_points, ) integer array of indices.
        """
        is_efficient = np.arange(costs.shape[0])
        n_points = costs.shape[0]
        next_point_index = 0  # Next index in the is_efficient array to search for
        while next_point_index < len(costs):
            nondominated_point_mask = np.any(costs < costs[next_point_index], axis=1)
            nondominated_point_mask[next_point_index] = True
            is_efficient = is_efficient[nondominated_point_mask]  # Remove dominated points
            costs = costs[nondominated_point_mask]
            next_point_index = np.sum(nondominated_point_mask[:next_point_index]) + 1
        if return_mask:
            is_efficient_mask = np.zeros(n_points, dtype=bool)
            is_efficient_mask[is_efficient] = True
            return is_efficient_mask
        else:
            return is_efficient

    def plot_pareto(self, costs, pareto_bool):

        import matplotlib.pyplot as plt
        plt.plot(costs[:, 0], costs[:, 1], '.')
        plt.plot(costs[pareto_bool, 0], costs[pareto_bool, 1], 'ro')
        plt.show()


