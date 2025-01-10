import sqlite3

class SQLMacro:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()


    def create_table(self, table_name, schema):
        columns = ", ".join([f"{col} {dtype}" for col, dtype in schema.items()])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.connection.commit()

    def insert(self, table_name, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        values = tuple(data.values())
        self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        self.connection.commit()

    def __getitem__(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return [dict(row) for row in self.cursor.fetchall()]

    def update(self, table_name, data, where=None):
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        values = list(data.values())
        query = f"UPDATE {table_name} SET {set_clause}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query, values)
        self.connection.commit()

    def delete(self, table_name, where=None):
        query = f"DELETE FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query)
        self.connection.commit()

    def get_all_tables_and_columns(self):
        # Get all table names in the database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table['name'] for table in self.cursor.fetchall()]

        # Get columns for each table
        table_columns = {}
        for table in tables:
            self.cursor.execute(f"PRAGMA table_info({table})")
            columns = [column['name'] for column in self.cursor.fetchall()]
            table_columns[table] = columns

        return table_columns

    def close(self):
        self.connection.close()
