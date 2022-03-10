import os

from eutils import Client

import enum


class NCBIDatabases(enum.Enum):
    """
    This will store the name of the databases and
    their respective codes and stuff
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, database, main_attribute):
        self.database = database
        self.main_attribute = main_attribute

    Nucleotides = 'nuccore', 'gbseqs'
    Genes = 'gene', ''


class EutilsConnection():
    ec = None
    database = None

    def __init__(self, database: NCBIDatabases):
        self.database = database
        self.db = database.database
        self.table = database.main_attribute
        self.ec = Client(api_key=os.environ.get("NCBI_API_KEY", None))

    def fetch_queries_ids(self, term: str, db=None, get_first=True) -> list:
        """
        This function will call the NCBI database "db" and look for the query specified on
        'term'. It could be as simple as "XM_537211". It will retrieve the query information
        with all the ids that match the search. If the get_first is True, then it will only get
        the first result.
        :param db:
        :param term:
        :param get_first:
        :return: a list of ids that match the search in given database
        """
        if get_first:
            retmax = 1
        else:
            retmax = 0
        if not db:
            db = self.db
        esr = self.ec.esearch(db=db, term=term, retmax=retmax)
        return esr.ids

    def get_id_information(self, db_id, db=None):
        """
        This funtion will take  and look for the complete information of that
        :param db: The database where we are going to look
        :param db_id: The id of the element in that database (maybe table???)
        :return:
        """
        if not db:
            db = self.db
        egs = self.ec.efetch(db=db, id=db_id)
        information = getattr(egs, self.table)  #
        return information[0]
