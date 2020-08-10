def process_vocabulary(vocabulary):
    """
    Processes vocabulary entries so they can be used for the tables
    :param vocabulary: vocbulary queryset
    :return: processed vocabulary
    """
    vocab_dict = {"entries": []}

    for row in vocabulary:
        # Add clickable Jisho links
        vocab_id = row.id
        kanji = f'<a href="https://jisho.org/search/{e}" target="_blank" rel="noopener">{e}</a>' if (
            e := row.kanji) else ""
        hiragana = f'<a href="https://jisho.org/search/{row.hiragana}" target="_blank" rel="noopener">{row.hiragana}</a>'
        english = e if (e := row.english) else ""

        entry = [vocab_id, kanji, hiragana, english]
        vocab_dict["entries"].append(entry)
    return vocab_dict
