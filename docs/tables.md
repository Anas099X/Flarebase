# Tables Documentation

## Creating Tables
Tables are the basic structure for organizing data in Flarebase.

### REST API
- **Create Table**: `POST /api/tables/create?name=table_name&fields=field1,field2,...`
- **Get All Tables**: `GET /api/tables`
- **Get Table Content**: `GET /api/tables/table_name`
- **Delete Table**: `DELETE /api/tables/table_name`

### Table Fields
Each table can have multiple fields that define the structure of records:
- Fields are created when the table is initialized
- Each field starts empty with an empty string value ("")
- Fields cannot be renamed after creation (you'll need to create a new table)

### Example

```fields={"users": {"1": {"name": ""},"2": {"email": ""},"3": {"age": ""}}}```

# Records Documentation

## Managing Records
Records are individual entries in tables that contain data for each defined field.

### REST API
- **Create Record**: `POST /api/record/create?table={table_name}&record={record_data}`
- **Delete Record**: `DELETE /api/record/delete?table={table_name}&record-id={id}`

### Record Structure
Each record in a table:
- Has a unique document ID
- Contains values for the fields defined in the table
- Can be updated or deleted individually
- Supports empty string values

### Example Record Data

```{'field1': 'value1', 'field2': 'value2'}```