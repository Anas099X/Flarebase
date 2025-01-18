from tinydb import TinyDB

# Initialize the database
db = TinyDB('flarebase.json')

# Access the 'areas' table
test = db.table('areas')

# Get the document with doc_id=2
result = test.get(doc_id=2)


for key, value in result.items():
    print(f"Key: {key}, Value: {value}")



