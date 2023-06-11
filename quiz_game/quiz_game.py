'''
a quiz game
'''

#import sqlite3
import os
from database import Database, ColumnSpec, ColumnType

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

