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

```json
{
  "field1": "value1",
  "field2": "value2"
}
```

### Example Usage

#### Creating a Record

```bash
curl -X POST "http://localhost:5001/api/record/create?table=users&record={'name': 'John', 'email': 'john@example.com'}"
```

#### Deleting a Record

```bash
curl -X DELETE "http://localhost:5001/api/record/delete?table=users&record-id=1"
```