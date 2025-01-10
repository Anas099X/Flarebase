from peewee import *
import json


class SimplePeeweeJSON:
    """Simplified interface for working with Peewee JSON data."""

    def __init__(self, db_name="simple_db.sqlite"):
        """Initialize the database and table."""
        self.db = SqliteDatabase(db_name)

        # Define the model connected to this database
        class BaseModel(Model):
            class Meta:
                database = self.db

        class JSONData(BaseModel):
            key = CharField(unique=True)  # Acts like a primary key
            value = TextField()  # Stores JSON as a string

        self.JSONData = JSONData

        # Connect to the database and create the table
        self.db.connect()
        self.db.create_tables([self.JSONData])

    def create(self, key, data):
        """Create a new JSON entry."""
        try:
            self.JSONData.create(key=key, value=json.dumps(data))
            return {"status": "success", "message": f"Entry '{key}' created."}
        except IntegrityError:
            return {"status": "error", "message": f"Key '{key}' already exists."}

    def fetch(self, key=None):
        """Fetch JSON data. If no key is provided, fetch all data."""
        if key:
            entry = self.JSONData.get_or_none(self.JSONData.key == key)
            if entry:
                return {"key": entry.key, "value": json.loads(entry.value)}
            else:
                return {"status": "error", "message": f"Key '{key}' not found."}
        else:
            return [
                {"key": entry.key, "value": json.loads(entry.value)}
                for entry in self.JSONData.select()
            ]

    def fetch_keys(self):
        """Fetch all available keys."""
        return [entry.key for entry in self.JSONData.select()]

    def update(self, key, data):
        """Update an existing JSON entry."""
        entry = self.JSONData.get_or_none(self.JSONData.key == key)
        if entry:
            entry.value = json.dumps(data)
            entry.save()
            return {"status": "success", "message": f"Entry '{key}' updated."}
        else:
            return {"status": "error", "message": f"Key '{key}' not found."}

    def delete(self, key):
        """Delete a JSON entry."""
        entry = self.JSONData.get_or_none(self.JSONData.key == key)
        if entry:
            entry.delete_instance()
            return {"status": "success", "message": f"Entry '{key}' deleted."}
        else:
            return {"status": "error", "message": f"Key '{key}' not found."}

    def add(self, key, new_data):
        """Add an object or element to an existing JSON entry."""
        entry = self.JSONData.get_or_none(self.JSONData.key == key)
        if entry:
            current_data = json.loads(entry.value)

            # Handle if the current data is a list
            if isinstance(current_data, list):
                current_data.append(new_data)
            # Handle if the current data is a dictionary
            elif isinstance(current_data, dict):
                if isinstance(new_data, dict):
                    current_data.update(new_data)
                else:
                    return {"status": "error", "message": "Cannot add non-dict to a dict entry."}
            else:
                return {"status": "error", "message": "Unsupported JSON structure for adding data."}

            entry.value = json.dumps(current_data)
            entry.save()
            return {"status": "success", "message": f"Data added to key '{key}'."}
        else:
            return {"status": "error", "message": f"Key '{key}' not found."}
