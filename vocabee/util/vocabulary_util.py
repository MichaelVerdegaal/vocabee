# TODO: can this be optimized? (maybe numpy, something else?)
def process_vocabulary(vocabulary):
    """
    Processes vocabulary entries so they can be used for the tables
    :param vocabulary: vocbulary queryset
    :return: processed vocabulary
    """
    vocab_dict = {"entries": []}

    for row in vocabulary:
        # Add clickable Jisho links
        row.kanji = f'<a href="https://jisho.org/search/{e}" target="_blank" rel="noopener">{e}</a>' if (
            e := row.kanji) else ""
        row.hiragana = f'<a href="https://jisho.org/search/{row.hiragana}" target="_blank" rel="noopener">{row.hiragana}</a>'
        row.english = e if (e := row.english) else ""

        # TODO: use complete JSON as datasource for table, instead of nested lists
        entry = [row.id, row.kanji, row.hiragana, row.english, [[e.id,
                                                                 e.sentence_jp,
                                                                 e.sentence_en] for e in row.examples]]
        vocab_dict["entries"].append(entry)
    return vocab_dict
