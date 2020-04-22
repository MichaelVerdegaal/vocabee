import json

from psycopg2 import connect, sql
from config import *


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


def process_vocabulary(vocabulary):
    """
    Processes vocabulary entries so they can be used for the tables
    :param vocabulary: vocabulary results as list of tuples
    :return: procssed vocabulary
    """
    N5 = {"entries": []}
    N4 = {"entries": []}
    N3 = {"entries": []}
    N2 = {"entries": []}
    N1 = {"entries": []}

    for row in vocabulary:
        # Add clickable Jisho links
        vocab_id = row[0]
        kanji = f'<a href="https://jisho.org/search/{e}" target="_blank">{e}</a>' if (e := row[1]) else ""
        hiragana = f'<a href="https://jisho.org/search/{row[2]}" target="_blank">{row[2]}</a>'
        english = e if (e := row[3]) else ""
        entry = [vocab_id, kanji, hiragana, english]

        level = row[4]
        # Split by JLPT level for performance reasons
        if level == "N5":
            N5["entries"].append(entry)
        elif level == "N4":
            N4["entries"].append(entry)
        elif level == "N3":
            N3["entries"].append(entry)
        elif level == "N2":
            N2["entries"].append(entry)
        elif level == "N1":
            N1["entries"].append(entry)
    return [N1, N2, N3, N4, N5]


def get_vocabulary():
    """
    Master function to get vocabulary and serialize it
    :return: Vocabulary entries as dictionary
    """
    connection = get_connection()
    cursor = get_cursor(connection)
    vocabulary = get_all_vocab(cursor)
    cursor.close()

    processed_vocabulary = process_vocabulary(vocabulary)
    for level in processed_vocabulary:
        json.dumps(level)
    return processed_vocabulary


vocabulary = get_vocabulary()
