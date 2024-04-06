import os
import genanki
import html
from os import getenv
from dotenv import load_dotenv

# Load enviroment variables from .env file
load_dotenv()

# Get the enviroment variables
INPUT_FOLDER = getenv("INPUT_FOLDER")
OUTPUT_FOLDER = getenv("OUTPUT_FOLDER")
MODEL_ID = int(os.getenv("MODEL_ID"))
DECK_ID = int(os.getenv("DECK_ID"))

# Define ANKI Model
model = genanki.Model(
    MODEL_ID,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ]
)

# Functions
def get_files_in_folder(file_path):
    """ Get the file list from a folder
    """
    files = os.listdir(file_path)
    return files

def read_markdown_file(file_path):
    """ Read a markdown file and extract the answer and the question
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    question = None
    answer_lines = []

    for line in lines:
        if line.startswith('##') and question is None:
            question = line[2:].strip()
        else:
            answer_lines.append(line.strip())
    
    answer = '<br>'.join(answer_lines)
    answer = answer.replace('<br>', '__BR__')
    question = html.escape(question)
    answer = html.escape(answer)
    answer = answer.replace('__BR__', '<br>')
    return question, answer

# Iterate over the folder in the input file
for folder_topic in get_files_in_folder(INPUT_FOLDER):
    topic_folder = os.path.join(INPUT_FOLDER, folder_topic.strip())
    # Create deck
    deck = genanki.Deck(
        DECK_ID,
        folder_topic
    )
    for file in get_files_in_folder(topic_folder):
        topic_file_folder = os.path.join(topic_folder, file.strip())
        # Read the markdown file
        question, answer = read_markdown_file(topic_file_folder)

        # Create note
        note = genanki.Note(
            model=model,
            fields=[question, answer]
        )

        # Add note to deck
        deck.add_note(note)

    # Create package
    package = genanki.Package(deck)

    # Write to Anki collection file (.apkg)
    package.write_to_file(os.path.join(getenv("OUTPUT_FOLDER"), f'{folder_topic}.apkg'))
