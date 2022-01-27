import unittest

from bs4 import BeautifulSoup

from paper_helper.paper_helper import EvaluatePapers


class Test(unittest.TestCase):

    def test_find_amount(self):
        helper = EvaluatePapers()
        with open("test_resources/ncbi_found_article.html", 'r') as file:
            html = file.read()
            html = BeautifulSoup(html, "html.parser")
        soup = helper.find_section_class_type(soup=html, object_type="em", class_name="amount")
        amount = helper.get_soup_text(soup)
        assert int(amount) == 128

