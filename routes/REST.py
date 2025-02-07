from main import *
import markdown
import ast


# ----------- Test ------------
@rt('/test')
def get():
    return (Button(
                cls="card bg-base-300 w-full hover:bg-warning hover:text-black border-2 border-black translate-x-1 translate-y-1.5 hover:translate-x-2 hover:translate-y-2 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-3 font-bold text-center mt-5 ml-1",
                hx_confirm="Are you sure you want to run this code",
                hx_post="/api/record/create?table=testggg&record={'field1': 'Anas', 'field2': 'NOTTT'}"
            ))

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
    

# ----------- Delete Table --------------
@rt("/api/tables/{table}")
def delete(table:str):
    json_output = db.drop_table(table)
    return Redirect("/")


# ----------- Create Record --------------
@rt("/api/record/create")
async def post(request: Request):
    # Parse query parameters
    query_params = request.query_params
    
    table_name = query_params.get("table")
    record = ast.literal_eval(query_params.get("record"))

    print(table_name, record)
    
    # Validate table name
    if not table_name:
        return Div("Table name cannot be empty.", cls="text-red-500")
    
    
    # Validate fields
    if not record:
        return Div("Fields cannot be empty.", cls="text-red-500")
    
    # add a record to table
    db.table(table_name).insert(record)
    
    # Redirect to the homepage
    return RedirectResponse("/", status_code=303)


# ----------- Delete Record --------------
@rt("/api/record/delete")
async def delete(request: Request):
    # Parse query parameters
    query_params = request.query_params
    
    table_name = query_params.get("table")
    record_id = query_params.get("record-id")

    print(table_name, record_id)
    
    # Validate table name
    if not table_name:
        return Div("Table name cannot be empty.", cls="text-red-500")
    
    # Check if table already exists
    if table_name in db.tables():
        return Div("Table already exists.", cls="text-red-500")
    
    
    # add a record to table
    table = db.table(table_name)
    table.remove(doc_ids=[record_id])
    
    # Redirect to the homepage
    return RedirectResponse("/", status_code=303)


# ----------- Documentation --------------

@rt("/docs/{doc}")
async def get(doc:str):
 with open(f'docs/{doc}.md', 'r', encoding="utf-8") as f:
        doc_content = markdown.markdown(f.read())  # Convert Markdown to HTML

 html_header = '''
 <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-dark.min.css">
 </head>
  <style>
        h1 {
            color: #efd156;
        }
    </style>    
 <body style="background-color: #0c1116; color: #b2ccd6;">
    <div class="markdown-body" id="markdown-content">
 '''
 html_markdown = f'''{doc_content}</div></body>'''

     

 return html_header + html_markdown
