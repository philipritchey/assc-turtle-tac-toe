'''
a database object.

'''

from typing import List, NewType, Dict, Union
import sqlite3
from dataclasses import dataclass
from enum import Enum


class ColumnType(Enum):
    '''
    the types a columnm can have
    '''
    INTEGER = int
    REAL = float
    TEXT = str
    BLOB = bytes
    NULL = None

@dataclass
class ColumnSpec:
    '''
    the specification of a column
    '''
    name: str
    type: ColumnType

@dataclass
class TableSpec:
    '''
    the specification of a table
    '''
    name: str
    columns: List[ColumnSpec]
    primary_key: str

class Column:
    '''
    represents a column

    a column has
    name: str
    type: Union[int, float, str, bytes, None]
    '''

Row = NewType('Row', Dict[str, Union[int, float, str, bytes, None]])

class Table:
    '''
    represents a table

    a table belongs to a database

    a Table has
    many columns (managed by database)
    auto-incrementing PK id (managed by DB)
    find(id) -> Row
    find_by(column_name, value) -> List[Row]
    create(values) -> Row or None
    update(id, values) -> Row or None
    delete(id) -> bool
    '''

    def __init__(self, database, name: str):
        self.database = database
        self.conn = self.database.conn
        self.name: str = name

    def find(self, id: int) -> sqlite3.Row:
        '''
        find a single record in the table by it's id

        Args:
            id: unique identifier (PK) of the record to find

        Returns:
            the record that was found, if any
        '''
        return self.conn.execute(
            f'''
            SELECT * FROM {self.name}
            WHERE id = ?
            ''',
            (id,)
        ).fetchone()

    def create(self, **kwargs) -> sqlite3.Row:
        '''
        create a single record in the table

        Args:
            a dictionary of column names and values

        Returns:
            the record that was inserted
        '''
        column_names = list(kwargs.keys())
        values = [kwargs[key] for key in column_names]
        command = f'INSERT INTO {self.name} ({", ".join(column_names)}) VALUES ({", ".join(["?"]*len(column_names))})'
        result = self.conn.execute(command, values)
        self.conn.commit()
        return self.conn.execute(
            f'''
            SELECT * FROM {self.name}
            WHERE id = ?
            ''',
            (result.lastrowid,)
        ).fetchone()

class Database:
    '''
    represents a database

    a Database has
    many tables (info about which is stored in a schema in the DB)
    create(table_name: str, column_specs: List[ColumnSpec])
    rename(table_name, new_name)
    rename_column(table_name, column_name, new_name)
    add_column(table_name, column_spec: ColumnSpec)
    drop_column(table_name, column_name)
    '''

    def __init__(self, db_name: str):
        # open connection
        self.conn = sqlite3.connect(f'./db/{db_name}.db')
        self.conn.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.conn.close()

    def create_table(self, table_name: str, column_specs: List[ColumnSpec]) -> Table:
        '''
        create a new table in the database

        Args:
            table_name: name of the new table
            columns_specs: a list of ColumnSpecs

        does nothing if the table name already exists
        '''
        columns = [
            'id INTEGER PRIMARY KEY AUTOINCREMENT'
        ]
        columns.extend([f'{column.name} {column.type.name}' for column in column_specs])
        columns.extend([
            'last_modified timestamp DEFAULT CURRENT_TIMESTAMP',
            'created timestamp DEFAULT CURRENT_TIMESTAMP'
        ])
        self.conn.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})
            '''
        )
        self.conn.commit()

        return Table(self, table_name)

    def rename_table(self, table_name: str, new_name: str) -> Table:
        '''
        rename a table

        Args:
            table_name: current name of table to rename
            new_name: new name of table
        '''
        self.conn.execute(
            f'''
            ALTER TABLE {table_name}
            RENAME TO {new_name}
            '''
        )
        self.conn.commit()

        return Table(self, table_name)

    def rename_column(self, table_name: str, column_name: str, new_name: str) -> Table:
        '''
        rename a column

        Args:
            table_name: name of the table which contains the column to rename
            column_name: name of the column to rename
            new_name: new name of column
        '''

        self.conn.execute(
            f'''
            ALTER TABLE {table_name}
            RENAME COLUMN {column_name} TO {new_name}
            '''
        )
        self.conn.commit()

        return Table(self, table_name)

    def add_column(self, table_name: str, column_spec: ColumnSpec) -> Table:
        '''
        add a column to a table

        Args:
            table_name: name of table to which to add the column
            column_spec: ColumnSpec defining the column to add
        '''
        column_def = f'{column_spec.name} {column_spec.type.name}'
        self.conn.execute(
            f'''
            ALTER TABLE {table_name}
            ADD COLUMN {column_def}
            '''
        )
        self.conn.commit()

        return Table(self, table_name)

    def drop_column(self, table_name: str, column_name: str) -> Table:
        '''
        remove a column from a table

        Args:
            table_name: name of table from which to remove the column
            column_name: name of column to remove
        '''
        self.conn.execute(
            f'''
            ALTER TABLE {table_name}
            DROP COLUMN {column_name}
            '''
        )
        self.conn.commit()

        return Table(self, table_name)
