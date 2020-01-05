import sqlite3
import prettytable

class ASQL(object):
    handle = sqlite3.connect('user.db')
    cursor = handle.cursor()

    def create_table(self):
        self.cursor.execute('create table arcaea ( qq int, ID int )')
        self.handle.commit()

    def find_user(self, qq):
        self.cursor.execute('select ID from arcaea where qq = ' + str(qq))
        id = self.cursor.fetchone()
        print(id)
        if len(id) == 0:
            return False, '000000001'
        return True, id[0]

    def insert_user(self, qq, ID):
        print('insert into arcaea values (' + str(qq) + ', ' + str(ID) + ')')
        self.cursor.execute('insert into arcaea values (' + str(qq) + ', ' + str(ID) + ')')
        self.handle.commit()
    
    def update_user(self, qq, ID):
        self.cursor.execute('update arcaea set ID = ' + str(ID) + ' where qq = ' + str(qq))
        self.handle.commit()

    def view(self):
        self.cursor.execute('select * from arcaea')
        table = prettytable.from_db_cursor(self.cursor)
        print(table)

    def delete_qq(self, qq):
        self.cursor.execute('delete from arcaea where qq = ' + str(qq))
