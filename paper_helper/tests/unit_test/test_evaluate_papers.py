import pytest


import numpy as np

from paper_helper.paper_helper import EvaluatePapers

short_csv = [{'database': 'Antagomirbase', 'year': '2011', 'Organism': 'Unspecified',
              'Website': 'http://bioinfopresidencycollegekolkata.edu.in/antagomirs.html', 'Download': 'No',
              'Available': 'No',
              'PubmedID': '21904438', "cite_number": 1},
             {'database': 'ARN', 'year': '2010', 'Organism': 'Unspecified', 'Website': 'http://210.27.80.93/arn/',
              'Download': 'No', 'Available': 'Yes', 'PubmedID': '27503118', "cite_number": 150},
             {'database': 'ARN', 'year': '2000', 'Organism': 'Unspecified', 'Website': 'http://210.27.80.93/arn/',
              'Download': 'No', 'Available': 'Yes', 'PubmedID': '27503118', "cite_number": 10}
             ]
evaluator = EvaluatePapers(short_csv)


def test_is_pareto_efficient():
    """
    Obtainded from https://github.com/QUVA-Lab/artemis/blob/peter/artemis/general/test_pareto_efficiency.py
    :return:
    """
    for n_costs in (2, 10):

        rng = np.random.RandomState(1234)

        costs = rng.rand(1000, n_costs)
        ixs = evaluator.is_pareto_efficient(costs)

        assert np.sum(ixs) > 0
        for c in costs[ixs]:
            assert np.all(np.any(c <= costs, axis=1))


def test_get_pareto_cites_year():
    papers = evaluator.get_pareto_cites_year(plot=True)
    pareto = [{'database': 'Antagomirbase', 'year': '2011',
               'Organism': 'Unspecified',
               'Website': 'http://bioinfopresidencycollegekolkata.edu.in/antagomirs.html',
               'Download': 'No', 'Available': 'No', 'PubmedID': '21904438', 'cite_number': 1},
              {'database': 'ARN', 'year': '2010', 'Organism': 'Unspecified',
               'Website': 'http://210.27.80.93/arn/',
               'Download': 'No', 'Available': 'Yes', 'PubmedID': '27503118', 'cite_number': 150}]
    assert papers == pareto
