#! usr/bin/env python3
from moduls import database
import sys
import datetime


db = database.DbManager('shopdb')


class CreateTableCommand:
    def execute(self):
        db.db_table_maker('bookmarker', {
            'id': 'INT GENERATED ALWAYS AS IDENTITY',
            'title': 'TEXT NOT NULL',
            'url': 'TEXT NOT NULL',
            'notes': 'TEXT',
            'added_date': 'TEXT NOT NULL'})


class AddBookmarkCommand:
    def execute(self, data):
        data['added_date'] = datetime.datetime.utcnow().isoformat()
        db.add_data('bookmarker', data)
        return 'bookmark is added!'


class SelectBookmarkCommand:
    def __init__(self, ordered_by='added_date'):
        self.ordered_by = ordered_by

    def execute(self):
        return db.to_select('bookmarker', order_by=self.ordered_by)


class DeleteBookmarkCommand:
    def execute(self, data):
        db.to_delete('bookmarker', {'id': data})
        return 'Bookmark is deleted!'


class QuitCommand:
    def execute(self):
        sys.exit()
