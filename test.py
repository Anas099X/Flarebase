from sqlmacro import SQLMacro
from peewee_lite import *
db = SimplePeeweeJSON("playful.sqlite")
for key in db.fetch_keys():
    print(key)
    print(db.fetch(key).get('value'))
 
