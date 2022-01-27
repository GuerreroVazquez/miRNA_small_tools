####This class will help with the analysis of articles reading in order to avoid manual searchs
#
import requests
from bs4 import BeautifulSoup


class EvaluatePapers:
    def __init__(self, url_address="https://example.com"):
        self.url = url_address
        req = requests.get(self.url)
        self.soup = BeautifulSoup(req.content, 'html.parser')
    #def get_number_cites(self):

    def find_all_section_class_type(self, soup=None, object_type="div", class_name="citedby-articles"):
        if not soup:
            soup = self.soup
        result_soup = soup.find_all(object_type, {"class": class_name})
        return result_soup

    def find_section_class_type(self, soup=None, object_type="div", class_name="citedby-articles"):
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
