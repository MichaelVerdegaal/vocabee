from fuzzywuzzy import fuzz


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
        row[
            'kana'] = f'<a href="https://jisho.org/search/{row["kana"]}" target="_blank" rel="noopener">{row["kana"]}</a>'
        row['english'] = row.get('english', '')
        return row

    vocabulary_dict = {'entries': [process_entry(e) for e in vocabulary]}
    return vocabulary_dict


def search_vocabulary(search_query, vocabulary_collection):
    """
    Fuzzy searches through vocabulary entries for matches.
    :param search_query: string of characters we'll trying to match
    :param vocabulary_collection: list of dicts of vocabulary entries to search through
    :return: dict of match and perfect match counts, perfect matches and fuzzy matches
    """
    search_query = search_query.lower()
    perfect_matches = []
    matches = []

    for row in vocabulary_collection['entries']:
        for col in ['english', 'kana', 'kanji', 'id']:
            ratio = fuzz.partial_ratio(search_query, str(row[col]).lower())
            match_item = {'matched_on': col, 'fuzzy_ratio': ratio, 'match_data': row}
            if ratio == 100:
                perfect_matches.append(match_item)
                break
            elif ratio >= 75:
                matches.append(match_item)
                break

    return {'perfect_match_count': len(perfect_matches),
            'match_count': len(matches),
            'perfect_matches': perfect_matches,
            'matches': matches}
