from fasthtml.common import *
from tinydb import TinyDB, Query
from urllib.parse import parse_qs
import secrets, json

# Initialize FastHTML app and TinyDB database
app = FastHTML(exts='ws')
rt = app.route

db = TinyDB("flarebase.json")
db_query = Query()

# Import REST routes
from routes import REST

# ------------------------------
# Helper Functions
# ------------------------------

def list_tables():
    """Generate a list of tables as clickable cards."""
    database = db.tables()
    cards = []
    for key in database:
        cards.append(
            Button(
                Div(key, cls="text-lg font-bold"),
                Div("Table", cls="text-md"),
                cls="card text-left bg-base-300 w-48 mb-3 hover:bg-warning hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 m-2",
                style="border-radius: 0;",
                hx_post=f"/view_table/{key}",
                hx_target="#records",
                hx_swap="innerHTML"
            )
        )
    return Div(*cards, cls="overflow-x-auto")


def keys_list(table):
    """Extract unique keys (columns) from a table."""
    all_keys = set()
    for doc in db.table(table).all():
        all_keys.update(doc.keys())
    return list(all_keys)


def list_records(table_input):
    """Display all records in a given table."""
    headers = keys_list(table_input)
    table = db.table(table_input)
    records = table.all()

    if not records:
        # Handle case where no records exist
        return Div(
            H3(f"Table {table_input}", cls="text-lg font-bold mb-4"),
            Div("No records available.", cls="text-gray-500"),
            cls="p-4"
        )

    # Add "Actions" column to headers
    headers.append("Actions")
    
    # Table headers
    table_head = Tr(
        *[Th(header, cls="text-left px-4 py-2 font-bold") for header in headers],
        cls="bg-base-300 border-2 border-black"
    )

    # Table rows with actions
    table_body = []
    for record in records:
        # Skip record if all its values are None or empty
        if all(value in (None, "") for value in record.values()):
            continue

        # Add data cells for each column
        row_data = [
            Td(record.get(header, ""), cls="px-4 py-2")
            for header in headers[:-1]  # Exclude the "Actions" column
        ]

        # Add action buttons
        actions = Td(
            Div(
                Label(
                    I(cls="ti ti-edit text-xl"),
                    cls="btn btn-sm btn-ghost btn-square hover:bg-warning",
                    hx_post=f"/fetch_fields/{table_input}/update/{record.doc_id}",
                    hx_target="#record-form-fields",
                    **{"for": "add-record-drawer"}
                ),
                Button(
                    I(cls="ti ti-trash text-xl text-red-600"),
                    cls="btn btn-sm btn-ghost btn-square hover:bg-warning",
                    hx_post=f"/delete_record/{table_input}/{record.doc_id}",
                    hx_target="#records",
                    hx_confirm="Are you sure you want to delete this record?"
                ),
                cls="flex gap-1"
            ),
            cls="px-4 py-2"
        )
        row_data.append(actions)

        # Append the row to the table body
        table_body.append(
            Tr(*row_data, cls="bg-base-300 hover:bg-warning hover:text-black")
        )

    # If no valid rows remain, show a message instead of an empty table
    if not table_body:
        return Div(
            H3(f"Table '{table_input}'", cls="text-lg font-bold mb-4"),
            Div("No valid records to display.", cls="text-gray-500"),
            cls="p-4"
        )
    
    # Return the table
    return Table(
        Thead(table_head),
        Tbody(*table_body),
        cls="table-auto border-2 border-black w-full bg-base-300 shadow-[8px_8px_0px_rgba(0,0,0,1)]"
    )


# ------------------------------
# Routes
# ------------------------------

@rt('/')
def get():
    # Drawer for adding a new table
    add_collection = Div(
        Div(
            Input(id="add-key-drawer", type="checkbox", cls="drawer-toggle"),
            Div(cls="drawer-content"),
            Div(
                Label(cls="drawer-overlay", **{"for": "add-key-drawer"}),
                Div(
                    H3("Add New Table", cls="text-xl font-bold flex justify-center"),
                    Form(
                        Div(
                            Div(
                                Label("Table Name:", cls="text-lg font-bold label"),
                                Input(
                                    type="text",
                                    name="table-name",
                                    placeholder="Table",
                                    cls="grow w-full border-black border-2 p-2.5 focus:outline-none focus:shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:bg-base-300 active:shadow-[2px_2px_0px_rgba(0,0,0,1)] rounded-md text-lg font-bold"
                                ),
                                cls="mb-4"
                            ),
                            Div(
                                Label("Fields:", cls="text-lg font-bold label"),
                                Div(
                                    Label(Input(type="text",name="field",cls="grow border-black border-2 p-2.5 focus:outline-none focus:shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:bg-base-300 active:shadow-[2px_2px_0px_rgba(0,0,0,1)] rounded-md text-lg font-bold",placeholder="Field"),
                                    cls=" flex items-center mb-2",id="fields-inputs"),
                                    id='fields',
                                    cls="h-32 overflow-y-auto"
                                ),
                                Label(
                                    "Add field",
                                    type="button",
                                    hx_post="/add_field",
                                    hx_target="#fields",
                                    hx_swap="beforeend",
                                    cls="card bg-base-300 w-32 hover:bg-warning hover:text-black border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center mt-3 text-lg font-bold",
                                    style="border-radius: 0;"
                                ),
                                cls="mb-4"
                            ),
                            Div(
                                Label(
                                    "Add table",
                                    type="button",
                                    hx_post="/create_table",
                                    hx_include="#fields-inputs input",
                                    cls="card rounded-none bg-base-300 w-full hover:bg-warning hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center text-lg font-bold",
                                    style="border-radius: 0;"
                                ),
                                cls="mt-12"
                            ),
                            cls="p-4"
                        ),
                        cls="bg-ghost rounded-lg"
                    ),
                    cls="menu text-base-content min-h-full w-96 p-4 bg-base-200"
                ),
                cls="drawer-side"
            ),
            cls="drawer drawer-end"
        )
    )

    # Updated Drawer for adding a new record with dynamic fields
    add_record = Div(
    Div(
        Input(id="add-record-drawer", type="checkbox", cls="drawer-toggle"),
        Div(cls="drawer-content"),
        Div(
            Label(cls="drawer-overlay", **{"for": "add-record-drawer"}),
            Div(
                H3("Add New Record",id="record-form-fields",cls="text-lg font-bold mb-4"),
                cls="menu bg-base-200 text-base-content min-h-full w-80 p-4"
            ),
            cls="drawer-side"
        ),
        cls="drawer drawer-end"
     )
    )

    # Table list as cards
    tables = Div(
        Div(
            Div("Tables", cls="text-lg text-warning font-bold w-48"),
            list_tables(),
            cls="flex flex-col gap-3"
        ),
        cls="overflow-y-auto p-4"
    )

    # Records section
    records = Div(
    Table(cls="table-auto w-full bg-ghost", id="records"),
    cls="w-56 bg-ghost flex-grow overflow-y-auto overflow-x-auto"
)

    return Div(
        Header(
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css"
            ),
            Link(
                href="https://cdn.jsdelivr.net/npm/daisyui@4.12.22/dist/full.min.css",
                rel="stylesheet",
                type="text/css"
            ),
            Script(src="https://cdn.tailwindcss.com")
        ),
        Head(
            Div(
                Div(I(cls="ti ti-comet text-4xl"), " Flarebase", cls="text-xl text-warning font-bold navbar-start"),
                A(I(cls="ti ti-brand-github text-3xl"),cls="text-warning m-2 font-bold navbar-end", href="https://github.com/Anas099X/Flarebase/blob/main/docs/Flarebase_Documentation.md"),
                cls="navbar bg-ghost"
            )   
        ),
        Body(
            Div(
                Div(
                    Div(
                        Div(I(cls="ti ti-database text-warning text-2xl"), " Database", cls="text-2xl text-warning font-bold"),
                        Div(
                            tables,
                            Div(cls="divider divider-horizontal"),
                            records,
                            cls="flex w-full max-w-6xl h-80"
                        ),
                        Label(
                            "Add table",
                            cls="card bg-base-300 w-32 hover:bg-warning hover:text-black border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center",
                                style="border-radius: 0;",
                            **{"for": "add-key-drawer"}
                        ),
                        cls="card-body"
                    ),
                    cls="card shadow-xl mx-auto w-full max-w-6xl bg-base-200"
                ),
                add_collection,
                add_record,
                cls="container mx-auto py-6 px-4"
            ),
            data_theme="dim",
            style="min-height:100vh;"
        ),
        cls="bg-base-100"
    )


@rt("/logo")
def get():
    return Div(
        Header(
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css"
            ),
            Link(
                href="https://cdn.jsdelivr.net/npm/daisyui@4.12.22/dist/full.min.css",
                rel="stylesheet",
                type="text/css"
            ),
            Script(src="https://cdn.tailwindcss.com")
        ),
    Div(
        Div(
           Div(I(cls="ti ti-comet text-warning text-8xl"), "Flarebase", cls="text-6xl text-warning font-bold"),
            cls="max-w-md"
        ),
        cls="hero-content text-center"
    ),
    cls="hero bg-base-100 min-h-screen"
)

@rt("/view_table/{selected_table}")
def post(selected_table: str):
    if not selected_table:
        return Div("No table selected.", cls="text-red-600")
    if selected_table not in db.tables():
        return Div(f"Table '{selected_table}' does not exist.", cls="text-red-600")

    # Return both the records and update the "Add record" and "Delete table" buttons
    return Div(
        # Display the GET API URL for the table
        Div(
            Div("GET", cls="badge badge-warning mr-1"),
            f"/api/tables/{selected_table}",
            cls="bg-base-300 w-full h-10 border-2 border-black shadow-md shadow-[3px_5px_0px_rgba(0,0,0,1)] p-1 font-bold text-center text-primary mb-3"
        ),
        # List records from the selected table
        list_records(selected_table),
        # Add record and delete table buttons
        Div(
            # Add record button
            Label(
                "Add record",
                cls="card bg-base-300 w-64 hover:bg-warning hover:text-black border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center mt-5",
                style="border-radius: 0;",
                hx_post=f"/fetch_fields/{selected_table}/add",
                hx_target="#record-form-fields",
                **{"for": "add-record-drawer"}
            ),
            # Delete table button
            Label(
                Div(cls="ti ti-trash text-xl text-red-600 text-center"),
                cls="card bg-base-300 w-12 h-12 hover:bg-warning hover:text-black border-2 border-black translate-x-1 translate-y-1.5 hover:translate-x-2 hover:translate-y-2 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-3 font-bold text-center mt-5 ml-1",
                style="border-radius: 0;",
                hx_confirm="Are you sure you want to delete this table?",
                hx_delete=f"/api/tables/{selected_table}"
            ),
            cls="flex justify-center"
        )
    )


@rt("/delete_table/{table}")
def post(table:str):
 db.drop_table(table)
 return Redirect("/")


@rt("/create_table")
async def post(request: Request):
    form = await request.form()
    table_name = form.get("table-name")
    
    if not table_name:
        return Div("Table name cannot be empty.", cls="text-red-600")
    
    if table_name in db.tables():
        return Div("Table already exists.", cls="text-red-600")
    
    table = db.table(table_name)
    
    for key, value in form.items():
        if key != "table-name":
            if not value:
                return Div("Fields cannot be empty.", cls="text-red-600")
            else:
                table.insert({value: ""})
    
    return Redirect("/")


@rt("/fetch_fields/{table_name}/{mode}/{record_id}")
def post(table_name: str ,mode:str ,record_id:int = None):
    """Fetch and display fields for the selected table"""
    if table_name == "default" or table_name not in db.tables():
        return Div("Please select a table first", cls="text-red-600")
    
    fields = keys_list(table_name)
    table = db.table(table_name)
    records = table.get(doc_id=record_id)
    if 'add' in mode:
     return Form(
        H3(f"Add record to {table_name}", cls="text-lg font-bold mb-4"),
        *[
            Div(
                Label(field.title() + ":", cls="label"),
                Input(
                    type="text",
                    name=field,
                    placeholder=f"Enter {field.lower()}",
                    cls="grow w-full border-black border-2 p-2.5 focus:outline-none focus:shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:bg-base-300 active:shadow-[2px_2px_0px_rgba(0,0,0,1)] rounded-md"
                ),
                cls="mb-4"
            )
            for field in fields if field  # Skip empty fields
        ],
        Label(
            "Add Record",
            type="submit",
            hx_post=f"/add_record/{table_name}",
            hx_target="#records",
            style="border-radius: 0;",
            cls="card bg-base-300 w-full hover:bg-warning hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-3 font-bold text-center mt-2"
        ),
        cls="p-4 bg-ghost rounded-lg"
    )

    elif 'update' in mode:
     return Form(
        H3(f"Update record of {table_name}", cls="text-lg font-bold mb-4"),
        *[
            Div(
                Label(key + ":", cls="label"),
                Input(
                    type="text",
                    name=key,
                    value=record,
                    placeholder=f"Enter {key.lower()}",
                    cls="grow w-full border-black border-2 p-2.5 focus:outline-none focus:shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:bg-base-300 active:shadow-[2px_2px_0px_rgba(0,0,0,1)] rounded-md"
                ),
                cls="mb-4"
            )  # Skip empty fields
            for key ,record in records.items()
        ][::-1],
        Label(
            "Update Record",
            type="submit",
            hx_post=f"/update_record/{table_name}/{record_id}",
            hx_target="#records",
            cls="card bg-base-300 w-full hover:bg-warning hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-3 font-bold text-center mt-2"
        ),
        cls="p-4 bg-ghost rounded-lg"
    )


@rt("/add_record/{table_name}")
async def post(request: Request, table_name: str):
    """Add a record to the specified table with dynamic fields"""
    if table_name not in db.tables():
        return Div("Table not found", cls="text-red-600")
    
    form = await request.form()
    
    # Create record dictionary from form data
    record = {key: value for key, value in form.items() if value.strip()}
    
    if not record:
        return Div("Please fill at least one field", cls="text-red-600 text-lg"),Div(
        Label(
            "Add record",
            cls="btn bg-black btn-outline w-64 mt-5 flex self-center",
            style="border-radius: 0;",
            hx_post=f"/fetch_fields/{table_name}/add",
            hx_target="#record-form-fields",
            **{"for": "add-record-drawer"}
        ),
        cls="flex justify-center"
        )
    
    # Insert the record
    db.table(table_name).insert(record)
    
    # Return updated table view
    return Div(
        Div(Div("GET",cls="badge badge-warning mr-1"),f"/api/tables/{table_name}",cls="bg-base-300 w-full h-10  border-2 border-black shadow-md shadow-[3px_5px_0px_rgba(0,0,0,1)] p-1 font-bold text-center mb-3"),
        list_records(table_name),
        Div(
        Label(
            "Add record",
            cls="card bg-base-300 w-64 hover:bg-warning hover:text-black border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center mt-5",
            style="border-radius: 0;",
            hx_post=f"/fetch_fields/{table_name}/add",
            hx_target="#record-form-fields",
            **{"for": "add-record-drawer"}
        ),
        Label(
            Div(cls="ti ti-trash text-xl text-red-600 text-center"),
            cls="card bg-base-300 w-12 h-12 hover:bg-warning hover:text-black  border-2 border-black translate-x-1 translate-y-1.5 hover:translate-x-2 hover:translate-y-2 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-3 font-bold text-center mt-5 ml-1",
            hx_delete=f"/api/tables/{table_name}"
        ),
        cls="flex justify-center"
        )
    )


@rt("/update_record/{table_name}/{record_id}")
async def post(request: Request, table_name: str, record_id: int):
    """Add a record to the specified table with dynamic fields"""
    if table_name not in db.tables():
        return Div("Table not found", cls="text-red-600")
    
    form = await request.form()
    
    # Create record dictionary from form data
    record = {key: value for key, value in form.items() if value.strip()}
    
    # Update the record
    table = db.table(table_name)
    table.update(record, doc_ids=[record_id])
    
    # Return updated table view
    return Div(
        Div(Div("GET",cls="badge badge-warning mr-1"),f"/api/tables/{table_name}",cls="bg-base-300 w-full h-10  border-2 border-black shadow-md shadow-[3px_5px_0px_rgba(0,0,0,1)] p-1 font-bold text-center mb-3"),
        list_records(table_name),
        Div(
        Label(
            "Add record",
            cls="card bg-base-300 w-64 hover:bg-warning hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center mt-5",
            style="border-radius: 0;",
            hx_post=f"/fetch_fields/{table_name}/add",
            hx_target="#record-form-fields",
            **{"for": "add-record-drawer"}
        ),
        Label(
            Div(cls="ti ti-trash text-xl text-red-600 text-center"),
            cls="card bg-base-300 w-12 h-12 hover:bg-warning hover:text-black  border-2 border-black translate-x-1 translate-y-1.5 hover:translate-x-2 hover:translate-y-2 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-3 font-bold text-center mt-5 ml-1",
            hx_delete=f"/api/tables/{table_name}"
        ),
        cls="flex justify-center"
        )
    )


@rt("/delete_record/{table_name}/{record_id}")
def post(table_name: str, record_id: int):
    """Delete a specific record from a table"""
    table = db.table(table_name)
    table.remove(doc_ids=[record_id])
    
    return Div(
        Div(Div("GET",cls="badge badge-warning mr-1"),f"/api/tables/{table_name}",cls="bg-base-300 w-full h-10  border-2 border-black shadow-md shadow-[3px_5px_0px_rgba(0,0,0,1)] p-1 font-bold text-center mb-3"),
        list_records(table_name),
        Div(
        Label(
            "Add record",
            cls="card bg-base-300 w-64 hover:bg-warning hover:text-black border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center mt-5",
            style="border-radius: 0;",
            hx_post=f"/fetch_fields/{table_name}/add",
            hx_target="#record-form-fields",
            **{"for": "add-record-drawer"}
        ),
        Label(
            Div(cls="ti ti-trash text-xl text-red-600 text-center"),
            cls="card bg-base-300 w-12 h-12 hover:bg-warning hover:text-black border-2 border-black translate-x-1 translate-y-1.5 hover:translate-x-2 hover:translate-y-2 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-3 font-bold text-center mt-5 ml-1",
            hx_delete=f"/api/tables/{table_name}"
        ),
        cls="flex justify-center"
        )
    )


@rt("/add_field")
def post():
    return Label(
        Input(type="text", name=f"field {secrets.token_urlsafe(5)}", cls="grow w-full border-black border-2 p-2.5 focus:outline-none focus:shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:bg-base-300 active:shadow-[2px_2px_0px_rgba(0,0,0,1)] rounded-md text-lg font-bold",placeholder="Field"),
        Button(
            hx_post="/remove_field",
            hx_target="#field-label",
            hx_swap="delete",
            cls="ti ti-trash text-2xl text-red-600 m-1"
        ),
        cls="flex items-center mb-2",
        id="field-label"
    )


@rt("/remove_field")
def post():
    return Div()


# Start the server
serve()