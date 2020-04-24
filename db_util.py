import json

from psycopg2 import connect, sql

from config import host, port, database, user, password


def get_connection():
    """
    Get database connection object
    :return: connection
    """
    return connect(host=host, port=port, database=database, user=user, password=password)


def get_cursor(connection):
    """
    Get database cursor object
    :param connection: database connection object
    :return: cursor
    """
    return connection.cursor()


def get_all_vocab(cursor):
    """
    Fetches all vocabulary entries from the database
    :param cursor: cursor object
    :return: vocabulary
    """
    cursor.execute("SELECT * FROM vocabulary")
    vocab = cursor.fetchall()
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
    return examples
