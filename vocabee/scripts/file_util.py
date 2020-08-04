import json

from vocabee.scripts.db_util import get_cursor, get_all_vocab


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
        kanji = f'<a href="https://jisho.org/search/{e}" target="_blank" rel="noopener">{e}</a>' if (
            e := row[1]) else ""
        hiragana = f'<a href="https://jisho.org/search/{row[2]}" target="_blank" rel="noopener">{row[2]}</a>'
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


def get_vocabulary(connection):
    """
    Master function to get vocabulary and serialize it
    :return: Vocabulary entries as dictionary
    """
    cursor = get_cursor(connection)
    vocabulary = get_all_vocab(cursor)

    processed_vocabulary = process_vocabulary(vocabulary)
    for level in processed_vocabulary:
        json.dumps(level)
    cursor.close()
    return processed_vocabulary
