import sql_operations as sql


def test_sql_connection():
    """
    This will just check that the connection is working

    :return:
    """

    sql.connect_sql()
    sql.disconnect_sql()
    pass


def test_query_connection():
    query = "select * from mirna_pre_mature LIMIT 1"
    result = sql.run_query(query=query)
    assert not result.empty
