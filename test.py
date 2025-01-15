from tinydb import *

db = TinyDB('sparkbase.json')

test = db.tables()

print(test)
