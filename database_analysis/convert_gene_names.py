# ###This class is going to rename the columns of gene in the new binding table ### #
# ### to unify the names.
import re

from logger import logger

from ncbi import eutilities
from database_analysis import sql_operations as sql
import logs
ncbi_connection = eutilities.EutilsConnection(eutilities.NCBIDatabases.Nucleotides)


def get_gene(provitional_gene):
    id = ncbi_connection.fetch_queries_ids(term=provitional_gene)
    if len(id) < 1:
        logger.error(f"The gene {provitional_gene} couldn't be found in NCBI")
        return None
    id = id[0]
    result = ncbi_connection.get_id_information(db_id=id)
    gene = result.gene
    if gene is None:
        logger.warning(f"There was no gene name for {provitional_gene} with Id {id}")
    logger.info(f"The name for {provitional_gene} will be {gene}")
    return gene

def get_genes_from_transcripts(provitional_gene):
    """

    :param provitional_gene:
    :return: dict
    """
    dict_transcript_gene = {}
    try:
        ids = ncbi_connection.fetch_queries_ids(term=provitional_gene)
        if len(ids) < 1:
            logger.error(f"The gene {provitional_gene} couldn't be found in NCBI")
            return None
        #for id in ids:
        #id = id[0]
        results = ncbi_connection.get_ids_information(db_id=ids)
        for result in results:
            locus = result.locus
            if locus in provitional_gene:
                gene = result.gene
                if gene is None:
                    logger.warning(f"There was no gene name for {provitional_gene} with Id {ids}")
                dict_transcript_gene[locus]=gene
                logger.info(f"The name for {provitional_gene} will be {gene}")
    except ValueError as ve:
        print(ve)
    except ConnectionError as ce:
        print(ce)
    except Exception as ex:
        print(ex)
    return dict_transcript_gene

def get_update_queries(genes, n=100, is_test=False):
    """
    Takes a list of transcripts, looks for the actual gene and save it on a temporal file.
    :param is_test:
    :param n:
    :param genes:
    :return:
    """

    with open("Temporal_file.txt", 'a') as f:
        groups = [genes[i:i + n] for i in range(0, len(genes), n)]
        mega_update_query_list=[]
        for genes in groups:
            update_query_list = []
            logger.info(f"Evaluating {genes}")
            gene_or = ' OR '.join(genes)
            real_names = get_genes_from_transcripts(gene_or)
            for key, item in real_names.items():
                update_query = f"UPDATE binding SET" \
                               f" mrna = '{item}'" \
                               f" WHERE mrna='{key}'; \n"
                update_query_list.append(update_query)
            if not is_test:
                f.writelines(update_query_list)
                f.flush()
            mega_update_query_list.extend(update_query_list)
    return mega_update_query_list

def update_queries(update_queries):
    """
    Takes a list of queries and updates the SQL
    :param update_queries:
    :return:
    """
    failed_updates = []
    for update_query in update_queries:

        rows = sql.run_query(query=update_query)
        logger.info(f" {rows} Affected")
        if rows < 1:
            gene = re.search("mrna = '(.*)' WHERE", update_query).group(1)
            logger.warning(f"Gene {update_query} couldn't been updated.")
            failed_updates.append(gene)
    return failed_updates

def convert_all_genes():
    query = "Select DISTINCT mrna from binding  where mrna like 'XM_%' or mrna like 'NM_%'"
    genes = sql.get_query(query=query)['mrna']
    if len(genes) < 1:
        logger.info(f"No genes found in binding with query {query}")
        return
    logger.info(f"Evaluating names of {len(genes)} genes.")
    genes = list(set(genes))

    update_query = get_update_queries(genes, n=250)
    # failed_updates = update_queries(update_query)
    failed_updates = len (update_query)
            # query = f"Select * from binding where mrna = '{real_name}' limit 10"
            # nuevo = sql.run_query(query=query)
    return failed_updates



def modify_gene():
    pass


if __name__ == '__main__':
    n = convert_all_genes()
    print (n)
    pass
