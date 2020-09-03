import genanki
from vocabee.util.db_util import get_examples_by_id
import random

vocabulary_model = genanki.Model(
    # ID's need to be hardcoded due to anki requirements
    1963760736,
    'JP model',
    fields=[
        {'name': 'Hiragana'},
        {'name': 'English'},
        {'name': 'Example'}
    ],
    templates=[
        {
            'name': 'Card',
            'qfmt': '<h1>{{Hiragana}}</h1>',
            'afmt': '{{FrontSide}}<hr id="answer"><h1>{{English}}</h1> <hr><h3>Example sentences</h3>{{Example}}',
        },
    ])


def get_example_sample(vocab_id):
    """
    Retrieves examples linked to a vocabulary entry and randomly samples a few
    :param vocab_id: vocabulary id
    :return: a list of up to 3 examples
    """
    examples = get_examples_by_id(vocab_id)
    example_count = len(examples)
    example_selection = []

    if example_count >= 3:
        example_selection = random.choices(examples, k=3)
    elif example_count == 2:
        example_selection = random.choices(examples, k=2)
    elif example_count == 1:
        example_selection = random.choices(examples, k=1)
    else:
        pass
    return example_selection


def create_example_note_string(example_list):
    """
    Creates a string which is used to represent example sentences in an anki note
    :param example_list: list of example sentences
    :return: string
    """
    note_string = ''
    for e in example_list:
        note_string += f'<br><strong><p>English: {e.sentence_en}</p></strong><p>Japanese: {e.sentence_jp}</p>'
    return note_string


def create_note(hiragana, english, vocab_id):
    """
    Creates an anki note (card)
    :param hiragana: hiragana text
    :param english: english text
    :param vocab_id: vocabulary id
    :return: anki note
    """
    examples = get_example_sample(vocab_id)
    example_string = ''
    if examples:
        example_string = create_example_note_string(examples)
    return genanki.Note(model=vocabulary_model, fields=[hiragana, english, example_string])


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
                           description='Japanese vocabulary deck from vocabee.xyz')
    return my_deck


def create_notelist(vocab_list):
    """
    Creates a list of notes based on a vocabulary list
    :param vocab_list: vocabulary list
    :return: list of anki notes
    """
    return [create_note(v.hiragana, v.english, v.id) for v in vocab_list]


def fill_deck(notelist, deck):
    """
    Adds a list of notes to a deck
    :param notelist: list of anki notes
    :param deck: anki deck
    """
    for note in notelist:
        deck.add_note(note)


def write_deck(deck, level):
    """
    TODO: See if we can find a way to change where the file is generated
    Writes an anki deck to a file at the root directory of the project
    :param deck: anki deck
    :param level: JLPT vocabulary level
    :return: name of the generated file
    """
    filename = f'vocabee{level}.apkg'
    genanki.Package(deck).write_to_file(filename)
    return filename


def create_deck_by_level(vocabulary, level):
    """
    Creates and writes to an anki deck from a vocabulary list
    :param vocabulary: vocabulary list
    :param level: JLPT vocabulary level
    :return: name of the generated file
    """
    new_deck = create_deck(level)
    notelist = create_notelist(vocabulary)
    fill_deck(notelist, new_deck)
    return write_deck(new_deck, level)
