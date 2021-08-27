import genanki

# ID's need to be hardcoded due to anki requirements
ANKI_MODEL_ID = 1963760736
ANKI_DECK_ID = 2076601992


def create_model(include_examples=True):
    fields = [{'name': 'Kana'},
              {'name': 'Kanji'},
              {'name': 'English'}]
    template = [{'name': 'Card',
                 'qfmt': '<h1>{{Kana}}{{Kanji}}</h1>',
                 'afmt': '{{FrontSide}}<hr id="answer"><h2>{{English}}</h2> '}]

    if include_examples:
        fields.append({'name': 'Example'})
        template[0]['afmt'] = '{{FrontSide}}<hr id="answer"><h2>{{English}}</h2> {{Example}}'

    vocabulary_model = genanki.Model(
        ANKI_MODEL_ID,
        'JP model',
        fields=fields,
        templates=template,
        css="h1, h2, h3, h4, h5, h6, p {text-align: center;}")
    return vocabulary_model


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


def create_deck(level):
    """
    Creates an anki deck
    :param level: JLPT vocabulary level
    :return: anki deck
    """
    # ID's need to be hardcoded due to anki requirements
    my_deck = genanki.Deck(deck_id=ANKI_DECK_ID,
                           name=f'Vocabee level {level}',
                           description='<h4 style="text-align: center">Japanese vocabulary deck from vocabee.xyz</h4>')
    return my_deck


def fill_deck(vocabulary_list, deck, model, include_examples):
    """
    Creates a notelist and add it to the deck
    :param vocabulary_list: vocabulary list
    :param deck: anki deck
    """

    def create_note(entry):
        """
        Creates an anki note (card)
        :param entry: vocabulary entry
        :return: anki note
        """
        kana = entry.kana
        english = entry.english
        kanji = f"/{entry.kanji}" if entry.kanji else ""

        fields = [kana, kanji, english]

        if include_examples:
            example_list = entry.examples
            example_string = create_example_note_string(example_list[:3])
            example_string = f'<hr><br><h2>Example usage</h2>{example_string}'
            fields.append(example_string)

        return genanki.Note(model=model, fields=fields)

    notelist = [create_note(v) for v in vocabulary_list]
    deck.notes = notelist


def create_deck_by_level(vocabulary, level, filename, include_examples):
    """
    Creates and writes to an anki deck from a vocabulary list
    :param vocabulary: vocabulary list
    :param level: JLPT vocabulary level
    :param filename: filename of deck
    :param include_examples: whether to include examples in the notes
    :return: name of the generated file
    """
    new_deck = create_deck(level)
    model = create_model(include_examples)
    fill_deck(vocabulary, new_deck, model, include_examples)
    genanki.Package(new_deck).write_to_file(filename)
