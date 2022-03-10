import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from logs import logger
config = {
    'user': 'root',
    'password': 'gato',
    'host': '127.0.0.1',
    'database': 'mirnadbs',
    'raise_on_warnings': True
}
cnx = None


def connect_sql():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None


def get_query(query: str):
    try:
        cnx = connect_sql()

        if cnx.is_connected():
            db_Info = cnx.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = cnx.cursor(buffered=True)
            cursor.execute("SET SESSION MAX_EXECUTION_TIME=10000")
            cursor.execute(query)
            record_dataframe = pd.read_sql(query, cnx)
            cnx.close()
            return record_dataframe

    except Exception as e:
        print("Error while connecting to MySQL", e)
        logger.error(e.msg)
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")


def run_query(query: str):
    try:
        cnx = connect_sql()

        if cnx.is_connected():
            db_Info = cnx.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = cnx.cursor(buffered=True)
            cursor.execute("SET SESSION MAX_EXECUTION_TIME=10000")
            cursor.execute(query)
            record_dataframe = cursor.statement
            affected_rows = cursor._affected_rows
            cnx.close()
            return affected_rows

    except Exception as e:
        print("Error while connecting to MySQL", e)
        logger.error(e.msg)
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")

def disconnect_sql():
    cnx.close()
