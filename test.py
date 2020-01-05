import sqlite3
import prettytable

a = sqlite3.connect('user.db')
c = a.cursor()

c.execute('select * from arcaea')
print(prettytable.from_db_cursor(c))