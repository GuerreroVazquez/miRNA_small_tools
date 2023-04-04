import pytest
from database_analysis.convert_gene_names import convert_all_genes, get_gene, get_genes_from_transcripts, \
    ncbi_connection
from database_analysis.map_gene_transcript import get_gene_names, convert_refseq_2_ensembl
from ncbi.eutilities import EutilsConnection
from ncbi.eutilities import NCBIDatabases
def test_get_gene_names():
    transcript_list = ["NM_001001398"]
    genes = get_gene_names(transcript_list)
    pass
    assert genes is not None
    assert len(genes)== len(transcript_list)

def test_convert_refseq_2_ensembl():
    transcript_list = ['NM_001001398',
                       'NM_001001398',
                       'NM_001001398',
                       'NM_001001398',
                       'NM_001001398',
                       'NM_001001398',
                       'NM_001001398']
    ensmbl_ids= convert_refseq_2_ensembl(transcript_list)
    assert ensmbl_ids is not None
    assert len(ensmbl_ids) == len(transcript_list)


def test_fetch_queries_ids():
    n = NCBIDatabases.Genes
    ec = EutilsConnection(n)
    x = ec.fetch_queries_ids("NM_001001398")
    y = ec.get_id_information(x)


def test_get_id_information():
    ec = EutilsConnection(NCBIDatabases.Nucleotides)
    id_n = 30560
    y = ec.get_id_information(id_n)
    a = 1

def test_convert_get_gene():
    provitional_gene='NM_001328693'
    gene = get_gene(provitional_gene)
    print(gene)
    assert gene == 'si:dkey-148a17.5'

def test_convert_get_gene_multiple():

    pmids = ['NM_001328693', 'NM_000014', 'NM_000018', 'NM_000022']
    provitional_gene = ' OR '.join(pmids)
    gene = get_genes_from_transcripts(provitional_gene)
    assert gene["NM_001328693"] == 'si:dkey-148a17.5'
    assert gene["NM_000018"] == 'ACADVL'


def get_ids_information():

    ids = [1779421316, 1519154122, 1518499068, 1040974839, 28996492, 28994628, 28994056, 957948862, 484275598]
    information = ncbi_connection.get_ids_information(db_id=ids)
    print(information)