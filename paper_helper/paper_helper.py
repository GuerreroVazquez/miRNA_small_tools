####This class will help with the analysis of articles reading in order to avoid manual searchs
#
import csv
import numpy as np
import logging

from paper_helper.common_tools import get_csv_into_dictionary, yml_to_dict, get_soup_from_html
from logging.config import dictConfig
from paper_helper.resources.file_adress import DatabasesDataset
import datetime

version_str = f'This run is running with versions:\n' \
              f'\t - csv {csv.__version__}' \
              f'\t - numpy {np.__version__}' \
              f'\t - logging {csv.__version__}' \
              f'Starting the {datetime.datetime.now()}'
logging.basicConfig(filename="paper_helper.log", level=logging.INFO)


class RecollectPapers:
    def __init__(self, url_address="https://pubmed.ncbi.nlm.nih.gov/", pubmed_ids=[]):
        self.url = url_address
        self.pubmed_ids = pubmed_ids
        self.category_list_address = r"C:\Users\crtuser\Documents\PhD\Project\repos\miRNA_small_tools\paper_helper" \
                                     r"\resources\data\db_categories.yml "
        self.information_list_address = r"C:\Users\crtuser\Documents\PhD\Project\repos\miRNA_small_tools\paper_helper" \
                                        r"\resources\data\db_information.yml"

    def get_number_cites(self, article_id):
        """
        This function should take the pubmed number and give the exact a
        :return: int
        """
        url = self.url + article_id
        soup = get_soup_from_html(url=url)
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

    def get_paper_data_from_file(self,
                                 file_name=r"C:\Users\crtuser\Documents\PhD\Project\repos\miRNA_small_tools\paper_helper\resources\data\papers_data.csv",
                                 paper_data=None):
        """
        Goes to the csv with the data of the papers to evaluate, gets the cite and the category and
        returns a list of dictionary where every entry is a paper.
        :param file_name:
        :param paper_data:
        :return: list dict
        """
        if not paper_data:
            logging.info(f"Reading file {file_name}")
            paper_data = get_csv_into_dictionary(file_name=file_name)
            logging.info(f"File sample: \n\t {paper_data[0]}")
        uno = paper_data[0]
        if not (
                "database" in paper_data[0].keys() and
                "PubmedID" in paper_data[0].keys() and
                "year" in paper_data[0].keys()):
            logging.error(f"CSV file is not complete")
            raise Exception("Missing necessary values in the csv file")
        logging.info(f'Getting number of cites and categories')
        with open("Temporal_file.tmp", 'w') as f:
            for paper in paper_data:
                try:
                    logging.info(f'getting {paper["database"]}')
                    if "cite_number" not in paper.keys():
                        paper["cite_number"] = self.get_number_cites(paper["PubmedID"])
                    if "categories" not in paper.keys():
                        paper["categories"] = self.get_categories(database_name=paper["database"])
                    if "information" not in paper.keys():
                        paper["information"] = self.get_information(database_name=paper["database"])
                except BaseException as e:
                    logging.error(f'')
                except Exception as e:
                    logging.error(f'Error {e}')
                    logging.error(f"Error occurred on {paper['database']}, with values {paper} replacing values with 0")
                    paper["cite_number"] = 'NA'
                    paper["categories"] = 'NA'
                    paper["information"] = 'NA'
                f.write(str(paper) + "\n")
                f.flush()

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
            if database_name in [x.lower() for x in categories[category]]:
                category_list.append(category+" - ")
        if len(category_list) == 0:
            category_list = "NA"
        return category_list

    def get_information(self, database_name=""):
        """
        Get the information from the category list (YML) and find all
         the information that a particular ddtabase is in
        :param database_name:
        :return: str list the information
        """
        information = yml_to_dict(self.information_list_address)
        database_name = database_name.lower()
        category_list = []
        for category in information.keys():
            if database_name in [x.lower() for x in information[category]]:
                category_list.append(category+" - ")
        if len(category_list) == 0:
            category_list = "NA"
        return category_list

    def get_all_categories(self, file_name="resources/data/papers_data.csv",
                           paper_data=None):
        if not paper_data:
            paper_data = self.get_paper_data_from_file(file_name)
        for database in paper_data:
            database["categories"] = self.get_categories(database_name=paper_data["database"])
            database["information"] = self.get_information(database_name=paper_data["database"])
        return paper_data

    def write_list_of_dict(self, list_dict, file_name="datasets_pareto_front.csv"):

        with open(file_name, 'w') as f:
            header = []
            for key in list_dict[0]:
                header.append(key)
                string_value = str(header).replace("[", "").replace("]", "").replace("'", "\"") + "\n"
            f.write(string_value)
            for element in list_dict:
                line = []
                for key, value in element.items():
                    if isinstance(value,str):
                        line.append(value.replace(",", "-"))
                    else:
                        line.append(str(value))
                string_value = str(line).replace("[", "").replace("]", "").replace("'", "\"") + "\n"
                f.write(string_value)

    def merge_two_dicts(self, x, y):
        z = x.copy()  # start with keys and values of x
        z.update(y)
        return z

    def merge_article_files_by(self, separate_by="PubmedID", merge_file_name="merge.csv", files_2_merge=[]):
        """
        This function will grab several csv files, grab their headers, create a header with the union of all of them.
        There are going to be a union of values as well, if new headers are introduce for a specific entry, that value
        will be fill out with NA
        :param separate_by:
        :param merge_file_name:
        :param files_2_merge:
        :return:
        """
        headers = []
        files = []
        for file in files_2_merge:
            dictionary = get_csv_into_dictionary(file)
            headers = headers + list(dictionary[0].keys())
            files = files + dictionary

        def sort_help(i):
            if separate_by in i.keys():
                return i[separate_by]
            else:
                return '-1'

        files = sorted(files, key=lambda i: sort_help(i))
        headers = list(dict.fromkeys(headers))
        new_list = []
        for index, line in enumerate(files):
            if index < len(files) - 1:
                if line[separate_by] == files[index + 1][separate_by]:
                    line = self.merge_two_dicts(line, files[index + 1])
                    del files[index + 1]
            tmp = {}
            for header in headers:
                if header in line.keys():
                    tmp[header] = line[header]
                else:
                    tmp[header] = "NA"
            new_list.append(tmp)
        self.write_list_of_dict(new_list, file_name=merge_file_name)


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
            try:
                cite_years.append([-int(paper["year"]), -int(paper["cite_number"])])
            except ValueError:
                cite_years.append([1992, 0])
                logging.error(f"Value error with article {paper['database']},"
                              f" year {paper['year']} and {paper['cite_number']} cites")

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
        logging.info(f"Getting pareto front of {len(costs)} elements")
        is_efficient = np.arange(costs.shape[0])
        n_points = costs.shape[0]
        next_point_index = 0  # Next index in the is_efficient array to search for
        while next_point_index < len(costs):
            nondominated_point_mask = np.any(costs < costs[next_point_index], axis=1)
            nondominated_point_mask[next_point_index] = True
            is_efficient = is_efficient[nondominated_point_mask]  # Remove dominated points
            costs = costs[nondominated_point_mask]
            logging.info(f"Pareto front {costs}")
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


def main():
    # dataset = DatabasesDataset.mirna_database.value
    dataset = DatabasesDataset.pareto_front_merge.value
    base = dataset.split(".")[0]
    logging.info('Starting process')
    helper = RecollectPapers()
    paper_info = get_csv_into_dictionary("resources/data/" + base + ".csv")
    papers = helper.get_paper_data_from_file(paper_data=paper_info, file_name=
    "resources/data/" + dataset)
    helper.write_list_of_dict(papers, "resources/data/papers_info/" + base + "_all.csv")
    ep = EvaluatePapers(papers_info=papers)
    pareto = ep.get_pareto_cites_year(plot=True)
    helper.write_list_of_dict(pareto, file_name="resources/pareto_fronts_databases/" + dataset)
    logging.info(f"The pareto front for this database was {pareto}")


if __name__ == "__main__":
    main()
