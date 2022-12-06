#! usr/bin/env python3
from moduls import database
import sys
import datetime

''' 
Մոդուլի այս հատվածը հավելվածի աբսրտակցիայի երկրորդ մակարդակն է։ Քանի որ ՏԲ հետ հիմնական կապը արդեն 
իսկ հաստատված է, այդ հատվածի դերը և ֆունկցիան կայանում է հիմնական և ձևատիպային հարցումների կազմությունը 
և տվյալների գրանցման կատարումը ՏԲ-ում։ Ուշադրություն դարձեք որ, այս հատվածի պատասխանատվությունը 
սահմանափակված է հենց իր կոդի ներսում, այն չի փորձում 'հասկանալ' կամ մոդիֆիկացնել մոդուլի մյուս հատվածը այն 
ուղղակի վերջնում է այդ մոդուլի պատրաստի լուծումները և կատարում է իրեն բաժին ընկած աշխատանքը։
'''


db = database.DbManager('webmarker_db')


# Կատարում է աղյուսակի ստեղծման, անհրաժեշտ սունյակների ստեղծուման հրամանաը։
class CreateTableCommand:
    def execute(self):
        db.db_table_maker('bookmarker', {
            'id': 'INT GENERATED ALWAYS AS IDENTITY',
            'title': 'TEXT NOT NULL',
            'url': 'TEXT NOT NULL',
            'notes': 'TEXT',
            'added_date': 'TEXT NOT NULL'})

        return '''SUCCESS ! (Don't need to do it again)'''


# Կատարում է նոր մարքի գրանցմումը ավելացնելով գրանցման ժամանակը։
class AddBookmarkCommand:
    def execute(self, data):
        data['added_date'] = datetime.datetime.utcnow().isoformat()
        db.add_data('bookmarker', data)
        return 'bookmark is added!'


# Կատարում է գրանցված մարքերի ցուցակը, դասավորում այն ըստ տրված չափանիշի։
class SelectBookmarkCommand:
    def __init__(self, ordered_by='added_date'):
        self.ordered_by = ordered_by

    def execute(self):
        return db.to_select('bookmarker', order_by=self.ordered_by)


# Կատարում է մարքի ջնջումը ըստ նրա ինդենտիֆիկացոն համարի։
class DeleteBookmarkCommand:
    def execute(self, data):
        db.to_delete('bookmarker', {'id': data})
        return 'Bookmark is deleted!'


# կատարում է հավելվածից դուրս գալու հրամանաը։
class QuitCommand:
    def execute(self):
        sys.exit()
