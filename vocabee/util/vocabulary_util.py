def process_vocabulary(vocabulary):
    """
    Processes vocabulary entries so they can be used for the tables
    :param vocabulary: vocbulary queryset
    :return: processed vocabulary
    """

    def process_entry(row):
        # Add clickable Jisho links
        kanji = f'<a href="https://jisho.org/search/{e}" target="_blank" rel="noopener">{e}</a>' if (
            e := row['kanji']) else ""
        hiragana = f'<a href="https://jisho.org/search/{row["hiragana"]}" target="_blank" rel="noopener">{row["hiragana"]}</a>'
        english = e if (e := row['english']) else ''
        return {'id': row['id'], 'kanji': kanji, 'hiragana': hiragana, 'english': english, 'examples': []}

    vocab_dict = {'entries': [process_entry(e) for e in vocabulary]}
    return vocab_dict
