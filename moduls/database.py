#! usr/bin/env python3
# -*- coding: <unicode> -*-

import psycopg2 as psy
from rich.console import Console
from rich.table import Table


class DbManager:

    # Կապ հաստատել ՏԲ հետ և պահպանել այդ վիճակը self.connection-ում։
    def __init__(self, base_name):
        self.connection = psy.connect(dbname=base_name)

    # ՏԲ հարցումը կատարող ֆունկցիա
    def execute(self, statement, values=None):
        with self.connection:
            cursor_connect = self.connection.cursor()
            cursor_connect.execute(statement, values or [])
        return cursor_connect

    # Կստեղծի ՏԲ աղյուսակը
    def db_table_maker(self, table_name, column):
        column_and_types = [f'{column_name} {column_type}'
                            for column_name, column_type in column.items()]
        self.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name} 
            ({', '.join(column_and_types)}); 
                '''
        )

    # Կպատրաստի և կփոխանցի տվյալները
    def add_data(self, table_name, data):
        placeholders = ', '.join(['%s'] * len(data))
        column_name = ', '.join(data.keys())
        column_value = tuple(data.values())
        self.execute(
            f'''
            INSERT INTO {table_name}
            ({column_name})
            VALUES ({placeholders});''',
            column_value
        )

    # Հարցում որը կջնջի անպետք մարքերը բայց նախապայմանով։
    def to_delete(self, table_name, criteria):
        placeholders = [f'{column} = %s' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self.execute(
            f"""
            DELETE from {table_name}
            WHERE {delete_criteria};
            """, tuple(criteria.values()))

    # Հարցում որը կկատարի ընտրման գործողություն։
    def to_select(self, table_name, criteria=None, order_by=None):
        criteria = criteria or {}

        query = f'SELECT * from {table_name}'

        if criteria:
            placeholders = [f'{column} = %s' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f'WHERE {select_criteria}'

        if order_by:
            query += f' ORDER BY {order_by};'

        rows = self.execute(query, tuple(criteria.values())).fetchall()

        table = Table(title='List of your Bookmarks', style='blue', )

        columns = {
            'Id': 9,
            'Title': 20,
            'Url': 35,
            'Notes': 25,
            'Date': 25
        }
        for key, value in columns.items():
            table.add_column(f'{key}', justify='right', style='red', width=value)

        for row in rows:
            table.add_row(f'{row[0]}', f'{row[1]}', f'{row[2]}', f'{row[3]}', f'{row[4]}')
        console = Console()
        console.print(table)

    def __del__(self):
        self.connection.close()
