from main import *

# ----------- Fetch Table --------------
@rt("/api/tables/{table}")
def get(table:str):
    json_output = db.table(table).all()
    return JSONResponse(json_output)


# ----------- Fetch All Tables ------------
@rt("/api/tables")
def get():
    json_output = list(db.tables())
    return JSONResponse(json_output)


# ----------- Create Table --------------
@rt("/api/tables/create")
async def post(request: Request):
    # Parse query parameters
    query_params = request.query_params
    
    table_name = query_params.get("name")
    fields = query_params.get("fields")

    print(table_name, fields)
    
    # Validate table name
    if not table_name:
        return Div("Table name cannot be empty.", cls="text-red-500")
    
    # Check if table already exists
    if table_name in db.tables():
        return Div("Table already exists.", cls="text-red-500")
    
    # Validate fields
    if not fields:
        return Div("Fields cannot be empty.", cls="text-red-500")
    
    # Create the table
    table = db.table(table_name)
    for field in fields.split(","):
        table.insert({field: ''})
    
    # Redirect to the homepage
    return RedirectResponse("/", status_code=303)

