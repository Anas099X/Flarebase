# Tables Documentation

## Creating Tables
Tables are the basic structure for organizing data in Flarebase.

### REST API
- **Create Table**: `POST /api/tables/create?name=table_name&fields=field1,field2,...`
- **Get All Tables**: `GET /api/tables`
- **Get Table Content**: `GET /api/tables/{table_name}`
- **Delete Table**: `DELETE /api/tables/{table_name}`
- **Search Table**: `GET /api/tables/search/{table}/{field}/{input}`

### Table Fields
Each table can have multiple fields that define the structure of records:
- Fields are created when the table is initialized
- Fields cannot be renamed after creation (you'll need to create a new table)

### Example

#### Creating a Table

```bash
curl -X POST "http://localhost:5001/api/tables/create?name=users&fields=name,email,age"
```

#### Getting All Tables

```bash
curl -X GET "http://localhost:5001/api/tables"
```

#### Getting Table Content

```bash
curl -X GET "http://localhost:5001/api/tables/users"
```

#### Deleting a Table

```bash
curl -X DELETE "http://localhost:5001/api/tables/users"
```

#### Searching a Table

```bash
curl -X GET "http://localhost:5001/api/tables/search/users/name/John"
```

### Example Table Data

```json
{
  "users": {
    "1": {"name": "John", "email": "john@example.com", "age": "30"},
    "2": {"name": "Jane", "email": "jane@example.com", "age": "25"}
  }
}
```

