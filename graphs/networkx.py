import networkx as nx
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import warnings

from database_analysis import sql_operations


def create_graph(mirnas, genes, relationsip):
    """
    This function will receive a list of genes and mirnas and create the network of them
    :param mirnas: List of string with the mirna names
    """
    G = nx.Graph()
    G.add_nodes_from(mirnas)
    G.add_nodes_from(genes)
    G.add_edges_from(relationsip)


def __init__():
    pass
