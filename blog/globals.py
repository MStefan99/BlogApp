import os
import sqlite3

path = os.path.join(os.getcwd(), 'database', 'db.sqlite')
DATABASE = sqlite3.connect(path, check_same_thread=False)  # TODO: check if thread-safe
DATABASE.row_factory = sqlite3.Row
DATABASE.cursor().execute('pragma foreign_keys = on')

COOKIE_NAME = 'MSTID'
