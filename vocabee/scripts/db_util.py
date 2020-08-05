import json
import os

from psycopg2 import connect, sql


def create_connection():
    """
    Attempt to create a dabase connection
    :return: connection
    """
    try:
        connection = connect(host=os.environ['host'],
                             port=os.environ['dbport'],
                             database=os.environ['database'],
                             user=os.environ['user'],
                             password=os.environ['password'])
        return connection
    except Exception as e:
        print(e)


def get_connection_if_exists(conn):
    """
    Passes connection if it exists, otherwise creates one
    :param conn: pyscopg2 connection object
    :return: connection
    """
    return conn if conn.closed == 0 else create_connection()


def get_cursor(connection):
    """
    Get database cursor object
    :param connection: database connection object
    :return: cursor
    """
    try:
        connection = get_connection_if_exists(connection)
        return connection.cursor()
    except Exception as e:
        print(e)


def get_all_vocab(cursor):
    """
    Fetches all vocabulary entries from the database
    :param cursor: cursor object
    :return: vocabulary
    """
    cursor.execute("SELECT * FROM vocabulary")
    vocab = cursor.fetchall()
    cursor.close()
    return vocab


def get_examples_by_id(cursor, vocab_id):
    """
    Retrieves example sentences based on the vocabulary id they're linked to
    :param cursor: cursor object
    :param vocab_id: vocabulary entry id
    :return: examples as valid json
    """
    cursor.execute(sql.SQL("SELECT * FROM example WHERE vocab_id = %s "), [vocab_id])
    examples = cursor.fetchall()
    examples = json.dumps(examples)
    cursor.close()
    return examples
