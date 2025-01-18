from tinydb import *

db = TinyDB('flarebase.json')

test = db.table('test')

test.update({"interests": "YEEES"}, doc_ids=[1])
