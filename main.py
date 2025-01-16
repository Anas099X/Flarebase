from fasthtml.common import *
from tinydb import TinyDB, Query
from urllib.parse import parse_qs
import secrets, json

app = FastHTML(exts='ws')
rt = app.route

# Initialize TinyDB database
db = TinyDB("cometbase.json")


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
                                    "Add Field",
                                    type="button",
                                    hx_post="/add_field",
                                    hx_target="#fields",
                                    hx_swap="beforeend",
                                    cls="card bg-base-300 w-full hover:bg-warning hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center mt-3 text-lg font-bold"
                                ),
                                cls="mb-4"
                            ),
                            Div(
                                Label(
                                    "Add Table",
                                    type="button",
                                    hx_post="/create_table",
                                    hx_include="#fields-inputs input",
                                    cls="card bg-base-300 w-full hover:bg-warning hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center text-lg font-bold"
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
                Div(I(cls="ti ti-comet text-warning text-3xl"), " Cometbase", cls="text-lg text-warning font-bold"),
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
                            "Add Table",
                            cls="card bg-base-300 w-32 hover:bg-warning hover:text-black border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center",
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


def list_tables():
    """Generate a list of tables as clickable cards."""
    database = db.tables()
    cards = []
    for key in database:
        cards.append(
            Button(
                Div(key, cls="text-lg font-bold"),
                Div("Table", cls="text-md"),
                cls="card bg-base-300 w-48 mb-3 hover:bg-warning hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 m-2",
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
        return Div(
            H3(f"Table '{table_input}'", cls="text-lg font-bold mb-4"),
            Div("No records available.", cls="text-gray-500"),
            cls="p-4"
        )

    # Table headers
    table_head = Tr(
        *[Th(header, cls="text-left px-4 py-2 font-bold") for header in headers],
        cls="bg-base-300 border-2 border-black"
    )

    # Table rows
    table_body = [
    Tr(
        *[
            Td(record.get(header), cls="px-4 py-2") 
            if record.get(header) not in (None, "")  # Check for None or empty string
            else '' 
            for header in headers
        ],
        cls="bg-base-300 hover:bg-warning hover:text-black"
    )
    for record in records]


    return Table(
        Thead(table_head),
        Tbody(*table_body),
        cls="table-auto border-2 border-black w-full bg-base-300 shadow-[8px_8px_0px_rgba(0,0,0,1)]"
    )


@rt("/view_table/{selected_table}")
def post(selected_table: str):
    if not selected_table:
        return Div("No table selected.", cls="text-red-500")
    if selected_table not in db.tables():
        return Div(f"Table '{selected_table}' does not exist.", cls="text-red-500")
    
    # Return both the records and update the add record button
    return Div(
        Div(Div("GET",cls="badge badge-warning mr-1"),f"/api/tables/{selected_table}",cls="bg-base-300 w-full h-10 border-2 border-black shadow-md shadow-[3px_5px_0px_rgba(0,0,0,1)] p-1 font-bold text-center text-primary mb-3"),
        list_records(selected_table),
        Div(
        Label(
            "Add record",
            cls="card bg-base-300 w-64 hover:bg-warning hover:text-black hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center mt-5",
            hx_post=f"/get_table_fields/{selected_table}",
            hx_target="#record-form-fields",
            **{"for": "add-record-drawer"}
        ),
        Label(
            Div(cls="ti ti-trash text-xl text-red-500 text-center"),
            cls="card bg-base-300 w-12 h-12 hover:bg-warning hover:text-black  border-2 border-black translate-x-1 translate-y-1.5 hover:translate-x-2 hover:translate-y-2 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-3 font-bold text-center mt-5 ml-1",
            hx_post=f"/delete_table/{selected_table}"
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
        return Div("Table name cannot be empty.", cls="text-red-500")
    
    if table_name in db.tables():
        return Div("Table already exists.", cls="text-red-500")
    
    table = db.table(table_name)
    
    for key, value in form.items():
        if key != "table-name":
            if not value:
                return Div("Fields cannot be empty.", cls="text-red-500")
            else:
                table.insert({value: ""})
    
    return Redirect("/")


@rt("/get_table_fields/{table_name}")
def post(table_name: str):
    """Fetch and display fields for the selected table"""
    if table_name == "default" or table_name not in db.tables():
        return Div("Please select a table first", cls="text-red-500")
    
    fields = keys_list(table_name)
    return Form(
        H3(f"Add Record to {table_name}", cls="text-lg font-bold mb-4"),
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
            cls="card bg-base-300 w-full hover:bg-warning hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-3 font-bold text-center mt-2"
        ),
        cls="p-4 bg-ghost rounded-lg"
    )



@rt("/add_record/{table_name}")
async def post(request: Request, table_name: str):
    """Add a record to the specified table with dynamic fields"""
    if table_name not in db.tables():
        return Div("Table not found", cls="text-red-500")
    
    form = await request.form()
    
    # Create record dictionary from form data
    record = {key: value for key, value in form.items() if value.strip()}
    
    if not record:
        return Div("Please fill at least one field", cls="text-red-600 text-lg"),Div(
        Label(
            "Add record",
            cls="btn bg-black btn-outline w-64 mt-5 flex self-center",
            hx_post=f"/get_table_fields/{table_name}",
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
            cls="card bg-base-300 w-64 hover:bg-warning hover:text-black  border-2 border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 font-bold text-center mt-5",
            hx_post=f"/get_table_fields/{table_name}",
            hx_target="#record-form-fields",
            **{"for": "add-record-drawer"}
        ),
        Label(
            Div(cls="ti ti-trash text-xl text-red-500 text-center"),
            cls="card bg-base-300 w-12 h-12 hover:bg-warning hover:text-black  border-2 border-black translate-x-1 translate-y-1.5 hover:translate-x-2 hover:translate-y-2 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-3 font-bold text-center mt-5 ml-1",
            hx_post=f"/delete_table/{table_name}"
        ),
        cls="flex justify-center"
        )
    )


@rt("/api/tables/{table}")
def get(table:str):
    json_output = db.table(table).all()
    return JSONResponse(json_output)

@rt("/api/tables")
def get():
    json_output = list(db.tables())
    return JSONResponse(json_output)


@rt("/add_field")
def post():
    return Label(
        Input(type="text", name=f"field {secrets.token_urlsafe(5)}", cls="grow w-full border-black border-2 p-2.5 focus:outline-none focus:shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:bg-base-300 active:shadow-[2px_2px_0px_rgba(0,0,0,1)] rounded-md text-lg font-bold",placeholder="Field"),
        Button(
            hx_post="/remove_field",
            hx_target="#field-label",
            hx_swap="delete",
            cls="ti ti-circle-x text-2xl text-base-200"
        ),
        cls="flex items-center mb-2",
        id="field-label"
    )

@rt("/remove_field")
def post():
    return Div()


serve()