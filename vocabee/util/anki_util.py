import datetime

import genanki

vocabulary_model = genanki.Model(
    # ID's need to be hardcoded due to anki requirements
    1963760736,
    'JP model',
    fields=[
        {'name': 'Kana'},
        {'name': 'Kanji'},
        {'name': 'English'},
        {'name': 'Example'}
    ],
    templates=[
        {
            'name': 'Card',
            'qfmt': '<h1>{{Kana}}{{Kanji}}</h1>',
            'afmt': '{{FrontSide}}<hr id="answer"><h2>{{English}}</h2> {{Example}}',
        },
    ],
    css="h1, h2, h3, h4, h5, h6, p {text-align: center;}")


def create_example_note_string(example_list):
    """
    Creates a string which is used to represent example sentences in an anki note
    :param example_list: list of example sentences
    :return: string
    """
    note_string = ''
    for e in example_list:
        note_string += f'<br> <strong><h3>Japanese: {e.sentence_jp}</h3></strong> <h3>English: {e.sentence_en}</h3>'
    return note_string


def create_note(example_list, kana, kanji, english):
    """
    Creates an anki note (card)
    :param example_list: list of example sentences
    :param kana: kana text
    :param kanji: kanji text
    :param english: english text
    :return: anki note
    """
    examples = example_list[:3]
    example_string = ''
    if examples:
        example_string = create_example_note_string(examples)
        example_string = f'<hr><br><h2>Example usage</h2>{example_string}'

    if kanji:
        kanji = f"/{kanji}"
    else:
        kanji = ""
    return genanki.Note(model=vocabulary_model, fields=[kana, kanji, english, example_string])


def create_deck(level):
    """
    Creates an anki deck
    :param level: JLPT vocabulary level
    :return: anki deck
    """
    # ID's need to be hardcoded due to anki requirements
    deck_id = 2076601991
    my_deck = genanki.Deck(deck_id=deck_id,
                           name=f'Vocabee level {level}',
                           description='<h4 style="text-align: center">Japanese vocabulary deck from vocabee.xyz</h4>')
    return my_deck


def fill_deck(vocabulary_list, deck):
    """
    Creates a notelist and add it to the deck
    :param vocabulary_list: vocabulary list
    :param deck: anki deck
    """
    notelist = [create_note(v.examples, v.kana, v.kanji, v.english) for v in vocabulary_list]
    deck.notes = notelist


def write_deck(deck, filename):
    """
    Writes an anki deck to a file at the root directory of the project
    :param deck: anki deck
    :param filename: filename of deck
    :return: name of the generated file
    """
    genanki.Package(deck).write_to_file(filename)
    return filename


def create_deck_by_level(vocabulary, level, filename):
    """
    Creates and writes to an anki deck from a vocabulary list
    :param vocabulary: vocabulary list
    :param level: JLPT vocabulary level
    :param filename: filename of deck
    :return: name of the generated file
    """
    new_deck = create_deck(level)
    fill_deck(vocabulary, new_deck)
    write_deck(new_deck, filename)
