# ###This class is going to rename the columns of gene in the new binding table ### #
# ### to unify the names.
import time

from ncbi import eutilities
from database_analysis import sql_operations as sql
from logs import logger

ncbi_connection = eutilities.EutilsConnection(eutilities.NCBIDatabases.Nucleotides)


def get_genes(provitional_gene):
    ids = ncbi_connection.fetch_queries_ids(term=provitional_gene, get_first =False)
    if len(ids) < 1:
        logger.error(f"The gene {provitional_gene} couldn't be found in NCBI")
        return None
    genes = []
    for gene in ids:
        result = ncbi_connection.get_id_information(db_id=gene)
        gene = result.gene
        if gene is None:
            logger.warning(f"There was no gene name for {provitional_gene} with Id {id}")
        genes.append(gene)
        time.sleep(1)
    return genes


def get_gene(provitional_gene):
    id = 0
    try:
        id = ncbi_connection.fetch_queries_ids(term=provitional_gene)
        if len(id) < 1:
            logger.error(f"The gene {provitional_gene} couldn't be found in NCBI")
            return None
        id = id[0]
        result = ncbi_connection.get_id_information(db_id=id)
        # gene = result.gene
        # if gene is None:
        gene = result.acv
    except Exception as e:
        logger.error( f"Assigning None on {provitional_gene}")
        gene = None
    if gene is None:
        logger.warning(f"There was no gene name for {provitional_gene} with Id {id}")
    logger.info(f"The name for {provitional_gene} will be {gene}")
    return gene


def convert_all_genes():
    query = "Select DISTINCT mrna from binding  where mrna like 'XM_%' or mrna like 'NM_0%' "
    genes = sql.get_query(query=query)['mrna']
    if len(genes) < 1:
        logger.info(f"No genes found in binding with query {query}")
        return
    logger.info(f"Evaluating names of {len(genes)} genes.")
    failed_updates = []
    full_query = ""
    blocks = 0
    with open("update_genes.sql", 'a') as f:
        for gene in genes:
            logger.info(f"Evaluating {gene}")
            real_name = get_gene(gene)
            if real_name is None:
                logger.error(f"There was no gene name for {gene}. Adding to watch out genes.")
                with open("watchout_genes.txt", 'a') as wo:
                    wo.write(gene + "\n")
                continue

            if gene is None:
                logger.info(f"The gene '{gene}' was not found in NCBI")
                continue
            if gene == real_name:
                logger.info(f"The gene '{gene}' is already the correct nomenclature")
                continue
            if len(real_name) > 30:
                logger.warning(f"The gene {gene} wants to be changed to {real_name} but the name "
                               f"is longer than 30 characters. The name will be truncated")
            # query = f"Select * from binding where mrna = '{gene}' limit 2"
            # viejo = sql.run_query(query=query)
            update_query = f"UPDATE binding SET" \
                           f" mrna = '{real_name}'" \
                           f" WHERE mrna='{gene}'; "
            full_query = full_query + update_query
            f.write(update_query + "\n")
            if blocks > 99:
                rows = sql.run_query(query=full_query)
                blocks = 0
                full_query = ""
                if rows < 1:
                    logger.warning(f"Section {full_query} couldn't been updated.")
                    failed_updates.append(gene)
            blocks = blocks + 1

        nuevo = sql.run_query(query=full_query)

    return failed_updates


def modify_gene():
    pass


if __name__ == '__main__':
    convert_all_genes()
    x = get_genes("sarcopenia ")
    print( x )
    pass
