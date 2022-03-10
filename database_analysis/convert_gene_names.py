# ###This class is going to rename the columns of gene in the new binding table ### #
# ### to unify the names.
from ncbi import eutilities
from database_analysis import sql_operations as sql
from logs import logger
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


def convert_all_genes():
    query = "Select DISTINCT mrna from binding  where mrna like 'XM_%' or mrna like 'NM_%'"
    genes = sql.get_query(query=query)['mrna']
    if len(genes) < 1:
        logger.info(f"No genes found in binding with query {query}")
        return
    logger.info(f"Evaluating names of {len(genes)} genes.")
    failed_updates = []
    with open("Temporal_file.txt", 'w') as f:
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
                           f" WHERE mrna='{gene}';"
            f.write(update_query + "\n")
            f.flush()
            rows = sql.run_query(query=update_query)
            logger.info(f" {rows} Affected")
            if rows < 1:
                logger.warning(f"Gene {gene} couldn't been updated.")
                failed_updates.append(gene)
            # query = f"Select * from binding where mrna = '{real_name}' limit 10"
            # nuevo = sql.run_query(query=query)
    return failed_updates



def modify_gene():
    pass


if __name__ == '__main__':
    convert_all_genes()
    pass
