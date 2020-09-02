import genanki

vocabulary_model = genanki.Model(
    # ID's need to be hardcoded due to anki requirements
    1963760736,
    'JP model',
    fields=[
        {'name': 'Hiragana'},
        {'name': 'English'},
    ],
    templates=[
        {
            'name': 'Card',
            'qfmt': '<h1>{{Hiragana}}</h1>',
            'afmt': '{{FrontSide}}<hr id="answer"><h2>{{English}}</h2>',
        },
    ])


def create_note(hiragana, english):
    return genanki.Note(model=vocabulary_model, fields=[hiragana, english])


def create_deck(level):
    # ID's need to be hardcoded due to anki requirements
    deck_id = 2076601991
    my_deck = genanki.Deck(deck_id=deck_id,
                           name=f'Vocabee level {level}',
                           description='')
    return my_deck


def create_notelist(vocab_list):
    return [create_note(v.hiragana, v.english) for v in vocab_list]


def fill_deck(notelist, deck):
    for note in notelist:
        deck.add_note(note)


def write_deck(deck, level):
    filename = f'vocabee{level}.apkg'
    genanki.Package(deck).write_to_file(filename)
    return filename


def create_deck_by_level(vocabulary, level):
    new_deck = create_deck(level)
    notelist = create_notelist(vocabulary)
    fill_deck(notelist, new_deck)
    return write_deck(new_deck, level)
