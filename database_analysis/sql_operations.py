import mysql.connector
from mysql.connector import errorcode
import pandas as pd

config = {
    'user': 'karen',
    'password': '123',
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


def run_query(query: str):
    try:
        cnx = connect_sql()
        if cnx.is_connected():
            db_Info = cnx.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = cnx.cursor()
            cursor.execute(query)
            record_dataframe = pd.read_sql(query, cnx)
            cnx.close()
            return record_dataframe

    except Exception as e:
        print("Error while connecting to MySQL", e)
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")


def disconnect_sql():
    cnx.close()
