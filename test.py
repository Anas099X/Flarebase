from tinydb import *
from tinydb.storages import *

db = TinyDB('playful.json')

User = Query()

table = db.table('ANAS099')

table.insert({"name": "randomname"})


print(db.table('Testtable').all())

