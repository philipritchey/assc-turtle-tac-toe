'''
a quiz game
'''

#import sqlite3
import os
import json
import sys
#from database import Database, ColumnSpec, ColumnType
from deck import Deck

'''
if os.path.exists('./db/test.db'):
    os.remove('./db/test.db')

with Database('test') as db:
    columns = [
        ColumnSpec('first_name', ColumnType.TEXT),
        ColumnSpec('last_name', ColumnType.TEXT),
    ]
    people = db.create_table('people', columns)
    philip = people.create(first_name = 'philip', last_name = 'ritchey')
    print([f'{key}: {philip[key]}' for key in philip.keys()])
    philip = people.find(philip['id'])
    print([f'{key}: {philip[key]}' for key in philip.keys()])
'''

'''
deck = Deck('US State Capitals')
us_state_capitals = [
    ('Alabama', 'Montgomery'),
    ('Alaska', 'Juneau'),
    ('Arizona', 'Phoenix'),
    ('Arkansas', 'Little Rock'),
    ('California', 'Sacramento'),
    ('Colorado', 'Denver'),
    ('Connecticut', 'Hartford'),
    ('Delaware', 'Dover'),
    ('Florida', 'Tallahassee'),
    ('Georgia', 'Atlanta'),
    ('Hawaii', 'Honolulu'),
    ('Idaho', 'Boise'),
    ('Illinois', 'Springfield'),
    ('Indiana', 'Indianapolis'),
    ('Iowa', 'Des Moines'),
    ('Kansas', 'Topeka'),
    ('Kentucky', 'Frankfort'),
    ('Louisiana', 'Baton Rouge'),
    ('Maine', 'Augusta'),
    ('Maryland', 'Annapolis'),
    ('Massachusetts', 'Boston'),
    ('Michigan', 'Lansing'),
    ('Minnesota', 'Saint Paul'),
    ('Mississippi', 'Jackson'),
    ('Missouri', 'Jefferson City'),
    ('Montana', 'Helena'),
    ('Nebraska', 'Lincoln'),
    ('Nevada', 'Carson City'),
    ('New Hampshire', 'Concord'),
    ('New Jersey', 'Trenton'),
    ('New Mexico', 'Santa Fe'),
    ('New York', 'Albany'),
    ('North Carolina', 'Raleigh'),
    ('North Dakota', 'Bismarck'),
    ('Ohio', 'Columbus'),
    ('Oklahoma', 'Oklahoma City'),
    ('Oregon', 'Salem'),
    ('Pennsylvania', 'Harrisburg'),
    ('Rhode Island', 'Providence'),
    ('South Carolina', 'Columbia'),
    ('South Dakota', 'Pierre'),
    ('Tennessee', 'Nashville'),
    ('Texas', 'Austin'),
    ('Utah', 'Salt Lake City'),
    ('Vermont', 'Montpelier'),
    ('Virginia', 'Richmond'),
    ('Washington', 'Olympia'),
    ('West Virginia', 'Charleston'),
    ('Wisconsin', 'Madison'),
    ('Wyoming', 'Cheyenne')
]
for state, capital in us_state_capitals:
    card = Card(state, capital)
    deck.add(card)
'''

print(f'+{"-"*78}+')

deck_names = None
cnt = 1
if os.path.exists('db/decks'):
    with open('db/decks', 'rt', encoding='utf-8') as file:
        deck_names = file.read().split('\n')
    for deck_name in deck_names:
        filename = ''
        for c in deck_name.strip():
            if c.isalnum():
                filename += c.lower()
            elif c.isspace():
                filename += '_'

        with open(f'db/{filename}.json', 'rt', encoding='utf-8') as file:
            deck = Deck.from_dict(json.load(file))
        print(f'({cnt:2d})',deck)
        if deck.any_due_now():
            print(f'       There are {deck.number_cards_due_now()} cards due for review.')
        else:
            print(f'       Next review is due {deck.next_card_due().due()}.')
else:
    print('No decks.')

print(f'+{"-"*78}+')

print('What do you want to do?')
print('(#) Review a deck (enter the number of the deck)')
print('(q) Quit the program')
answer = input('? ')
if answer.strip().isnumeric():
    deck_name = deck_names[int(answer.strip()) - 1]
elif answer.strip().lower() == 'q':
    print('Goodbye!')
    sys.exit(0)
else:
    print('Invalid input.')
    # TODO(pcr): don't leave, reprompt
    sys.exit(0)

filename = ''
for c in deck_name:
    if c.isalnum():
        filename += c.lower()
    elif c.isspace():
        filename += '_'

with open(f'db/{filename}.json', 'rt', encoding='utf-8') as file:
    deck = Deck.from_dict(json.load(file))

print()
print(deck_name)
print('-'*len(deck_name))
print(f'There are {deck.number_cards_due_now()} cards due for review.')

if deck.any_due_now():
    for card in deck.due_now():
        if deck.card_prefix:
            print(deck.card_prefix)
        print(card)
        answer = input('? ').strip().lower()
        if answer == card.back.lower():
            print('Correct!')
            card.recall_success()
        else:
            print('Incorrect. The correct answer is:')
            print(repr(card.back))
            card.recall_failure()

    with open(f'db/{filename}.json', 'wt', encoding='utf-8') as file:
        file.write(json.dumps(deck.to_dict()))