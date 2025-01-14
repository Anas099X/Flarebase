from fasthtml.common import *
from tinydb import TinyDB, Query
from urllib.parse import parse_qs
import secrets

app = FastHTML(exts='ws')
rt = app.route

# Initialize TinyDB database
db = TinyDB("sparkbase.json")


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
                    H3("Add New Table", cls="text-lg font-bold flex justify-center"),
                    Form(
                        Div(
                            Div(
                                Label("Table Name:", cls="label"),
                                Input(
                                    type="text",
                                    name="table-name",
                                    placeholder="Table",
                                    cls="input input-bordered w-full"
                                ),
                                cls="mb-4"
                            ),
                            Div(
                                Label("Fields:", cls="label"),
                                Div(
                                    Label(Input(type="text",name="field",cls="grow",placeholder="Field"),
                                    cls="input input-bordered flex items-center mb-2",id="fields-inputs"),
                                    id='fields',
                                    cls="h-32 overflow-y-auto"
                                ),
                                Button(
                                    "Add Field",
                                    type="button",
                                    hx_post="/add_field",
                                    hx_target="#fields",
                                    hx_swap="beforeend",
                                    cls="btn bg-yellow btn-outline w-full mt-3"
                                ),
                                cls="mb-4"
                            ),
                            Div(
                                Button(
                                    "Add Table",
                                    type="button",
                                    hx_post="/create_table",
                                    hx_include="#fields-inputs input",
                                    cls="btn bg-yellow btn-outline w-full"
                                ),
                                cls="mt-12"
                            ),
                            cls="p-4"
                        ),
                        cls="bg-ghost rounded-lg"
                    ),
                    cls="menu text-base-content min-h-full w-96 p-4 bg-orange-500"
                ),
                cls="drawer-side"
            ),
            cls="drawer drawer-end"
        )
    )

    # Drawer for adding a new record (updated to include table selection)
    add_record = Div(
        Div(
            Input(id="add-record-drawer", type="checkbox", cls="drawer-toggle"),
            Div(cls="drawer-content"),
            Div(
                Label(cls="drawer-overlay", **{"for": "add-record-drawer"}),
                Div(
                    H3("Add New Record", cls="text-lg font-bold mb-4"),
                    Form(
                        Div(
                            Div(
                                Label("Record Name:", cls="label"),
                                Input(
                                    type="text",
                                    name="record_name",
                                    placeholder="Enter record name",
                                    cls="input input-bordered w-full"
                                ),
                                cls="mb-4"
                            ),
                            Div(
                                Label("Description:", cls="label"),
                                Textarea(
                                    name="description",
                                    placeholder="Enter description",
                                    cls="textarea textarea-bordered w-full"
                                ),
                                cls="mb-4"
                            ),
                            Div(
                                Label("Select Table:", cls="label"),
                                Select(
                                    *[Option(table, value=table) for table in db.tables()],
                                    name="table",
                                    cls="select select-bordered w-full"
                                ),
                                cls="mb-4"
                            ),
                            Div(
                                Button(
                                    "Add Record",
                                    type="submit",
                                    hx_post="/add_record",
                                    hx_trigger="load",
                                    hx_swap="none",
                                    cls="btn btn-success w-full"
                                ),
                                cls="mt-4"
                            ),
                            cls="p-4"
                        ),
                        cls="bg-base-200 rounded-lg"
                    ),
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
            Div("Tables", cls="text-lg text-yellow-300 font-bold w-48"),
            list_collection(),
            cls="flex flex-col gap-3"
        ),
        cls="overflow-hidden overflow-y-auto p-4"
    )

    # Records section (updated dynamically using htmx)
    records = Div(
                Table(cls="table-auto w-full bg-ghost",id="records"),
                    Label(
                    "Add record",
                    cls="btn bg-black btn-outline w-64 mt-5",
                    **{"for": "add-record-drawer"}
                    ),
                    cls="card w-56 bg-ghost rounded-box flex-grow place-items-center overflow-x-clip")


    return (
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
                Div(I(cls="ti ti-comet text-yellow-200 text-3xl"), " SparkBase", cls="text-lg text-yellow-200 font-bold"),
                cls="navbar bg-orange-500"
            )
        ),
        Body(
            Div(
                Div(
                    Div(
                        Div(I(cls="ti ti-database text-yellow-200 text-2xl"), " Database", cls="text-2xl text-yellow-200 font-bold"),
                        Div(
                            tables,
                            Div(cls="divider divider-horizontal"),
                            records,
                            cls="flex w-full max-w-6xl h-80"
                        ),
                        Label(
                            "Add Table",
                            cls="btn bg-black btn-outline w-48",
                            **{"for": "add-key-drawer"}
                        ),
                        cls="card-body"
                    ),
                    cls="card shadow-xl mx-auto w-full max-w-6xl bg-orange-500"
                ),
                add_collection,
                add_record,
                cls="container mx-auto py-6 px-4"
            ),
            data_theme="light",
            style="min-height:100vh;"
        )
    )


def list_collection():
    """
    Generate a list of tables as clickable cards.
    """
    database = db.tables()
    cards = []
    for key in database:
        cards.append(
            Button(
                Div(key, cls="text-lg font-bold"),  # Table name
                Div("Table", cls="text-md"),
                cls="card bg-yellow-300 w-48 mb-3 hover:bg-yellow-400 bg-white border border-black hover:translate-x-1 hover:translate-y-1 shadow-md hover:shadow-[3px_5px_0px_rgba(0,0,0,1)] p-4 m-2",
                hx_post=f"/view_table/{key}",
                hx_target="#records",
                hx_swap="innerHTML"
            )
        )
    return Div(*cards, cls="overflow-x-auto")


def keys_list(table):
    """
    Extract unique keys (columns) from a table.
    """
    all_keys = set()
    for doc in db.table(table).all():
        all_keys.update(doc.keys())
    return list(all_keys)


def list_records(table_input):
    """
    Display all records in a given table.
    """
    headers = keys_list(table_input)
    table = db.table(table_input)
    records = table.all()

    if not records:
        # Display empty table design
        return Div(
            H3(f"Table '{table_input}'", cls="text-lg font-bold mb-4"),
            Div("No records available.", cls="text-gray-500"),
            cls="p-4"
        )

    # Table headers
    table_head = Tr(
        *[Th(header, cls="text-left px-4 py-2 font-bold") for header in headers],
        cls="bg-yellow-300"
    )

    # Table rows
    table_body = [
        Tr(
            *[Td(record.get(header, "N/A"), cls="px-4 py-2") for header in headers],
            cls="bg-yellow-300 hover:bg-yellow-400 hover:translate-x-1"
        )
        for record in records
    ]

    return Table(
        Thead(table_head),
        Tbody(*table_body),
        cls="table-auto w-full bg-ghost"
    )


@rt("/view_table/{selected_table}")
def post(selected_table: str):
    if not selected_table:
        return Div("No table selected.", cls="text-red-500")
    if selected_table not in db.tables():
        return Div(f"Table '{selected_table}' does not exist.", cls="text-red-500")
    return list_records(selected_table)


@rt("/create_table")
async def post(request: Request):
    # Get form data using FastHTML's form data handling
    form = await request.form()
    
    # Get collection name from form data
    table_name = form.get("table-name")
    
    if not table_name:
        return Div("Table name cannot be empty.", cls="text-red-500")
    
    if table_name in db.tables():
        return Div("Table already exists.", cls="text-red-500")
    
    # Create the table
    table = db.table(table_name)
    
    # Process the form data
    for key, value in form.items():
        if key != "table-name":  # Skip the collection name field
            table.insert({value: ""})
    
    return Redirect("/")


@rt("/add_record")
def post(record_name: str, description: str, table: str):
    """
    Add a new record to the selected table.
    """
    if not record_name or not description or not table:
        return Div("Invalid input!", cls="text-red-500")
    if table not in db.tables():
        return Div(f"Table '{table}' does not exist.", cls="text-red-500")
    db.table(table).insert({"name": record_name, "description": description})
    return RedirectResponse("/", status_code=303)


@rt("/add_field")
def post():
 return Label(Input(type="text",name=f"field {secrets.token_urlsafe(5)}",cls="grow",placeholder="Field"),
        Button(hx_post="/remove_field",hx_target="#field-label",hx_swap="delete",cls="ti ti-circle-x text-2xl text-orange-500"),
        cls="input input-bordered flex items-center mb-2",id="field-label")

@rt("/remove_field")
def post():
 return Div()

serve()
