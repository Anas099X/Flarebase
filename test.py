from tinydb import *

db = TinyDB('sparkbase.json')


print(db.drop_table('test312'))
