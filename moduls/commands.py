#! usr/bin/env python3
import database
import datetime
import sys

db = database.DbManager('shopdb')


class CreateTableCommand:
    def table_execute(self):
        db.db_table_maker('bookmarker', {
            'id': 'INT GENERATED ALWAYS AS IDENTITY',
            'title': 'TEXT NOT NULL',
            'url': 'TEXT NOT NULL',
            'notes': 'TEXT',
            'added_date': 'TEXT NOT NULL'})


class AddBookmarkCommand:
    def bookmark_add_execute(self, data):
        data['added_date'] = datetime.datetime.utcnow().isoformat()
        db.add_data('bookmarker', data)
        return 'bookmark is added!'


class SelectBookmarkCommand:
    def __int__(self, ordered_by='added_date'):
        self.ordered_by = ordered_by

    def select_bookmark_execute(self):
        return db.to_select('bookmarker', order_by=self.ordered_by).fetchall()


class DeleteBookmarkCommand:
    def bookmark_delete_execute(self, data):
        db.to_delete('bookmarker', {'id': data})
        return 'Bookmark is deleted!'


class QuitCommand:
    def execute(self):
        sys.exit()
