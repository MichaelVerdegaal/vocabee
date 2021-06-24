def process_vocabulary(vocabulary):
    """
    Processes vocabulary entries so they can be used for the tables
    :param vocabulary: vocbulary queryset
    :return: processed vocabulary
    """

    def process_entry(row):
        # Add clickable Jisho links
        row = dict(row)
        row['kanji'] = f'<a href="https://jisho.org/search/{e}" target="_blank" rel="noopener">{e}</a>' if (
            e := row['kanji']) else ""
        row['kana'] = f'<a href="https://jisho.org/search/{row["kana"]}" target="_blank" rel="noopener">{row["kana"]}</a>'
        row['english'] = row.get('english', '')
        return row

    vocabulary_dict = {'entries': [process_entry(e) for e in vocabulary]}
    return vocabulary_dict
