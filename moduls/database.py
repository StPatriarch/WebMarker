#! usr/bin/env python3
# -*- coding: <unicode> -*-
import psycopg as psy


class DbManager:

    # Կապ հաստատել ՏԲ հետ և պահպանել այդ վիճակը self.connection-ում։
    def __init__(self, base_name):
        self.connection = psy.connect(dbname=base_name)

    # ՏԲ հարցումը կատարող ֆունկցիա
    def _query_execute(self, statement, values=None):
        with self.connection:
            cursor_connect = self.connection.cursor()
            cursor_connect.execute(statement, values or [])
        return cursor_connect

    # Կստեղծի ՏԲ աղյուսակը
    def db_table_maker(self, table_name, column):
        column_and_types = [f'{column_name} {column_type}'
                            for column_name, column_type in column.items()]
        self._query_execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name} 
            ({', '.join(column_and_types)}); 
                '''
        )

    # Կպատրաստի և կփոխանցի տվյալները
    def add_data(self, table_name, data):
        placeholders = ', '.join('?' * len(data))
        column_name = ', '.join(data.keys())
        column_value = tuple(data.values())
        self._query_execute(
            f'''
            INSERT INTO {table_name}
            ({column_name})
            VALUES ({placeholders});''',
            column_value
        )

    # Հարցում որը կջնջի անպետք մարքերը բայց նախապայմանով։
    def to_delete(self, table_name, criteria):
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._query_execute(
            f"""
            DELETE from {table_name}
            WHERE {delete_criteria};
            """, tuple(criteria.values()))

    # Հարցում որը կկատարի ընտրման գործողություն։
    def to_select(self, table_name, criteria=None, order_by=None):
        criteria = criteria or {}

        query = f'SELECT * FROM {table_name}'

        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f'WHERE {select_criteria}'

        if order_by:
            query += f'ORDER BY {order_by}'

        self._query_execute(query, tuple(criteria.values()))

    def __del__(self):
        self.connection.close()
