from tinydb import *

db = TinyDB('cometbase.json')

test = db.table('areas2')

print(test.all())
