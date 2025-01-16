from tinydb import *

db = TinyDB('cometbase.json')


print(db.drop_table('test312'))
