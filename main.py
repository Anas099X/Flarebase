from peewee_lite import *
from fasthtml.common import *

app = FastHTML(exts='ws')
rt = app.route

db = SimplePeeweeJSON("playful.sqlite")



@rt('/')
def get():
 
 add_collection = Div(
        Div(
            # Drawer input (toggle)
            Input(
                id="add-collection-drawer",
                type="checkbox",
                cls="drawer-toggle"
            ),
            # Drawer content
            Div(
                
                cls="drawer-content"
            ),
            # Drawer sidebar (Form for adding collections)
            Div(
                Label(
                    cls="drawer-overlay",
                    **{"for": "add-collection-drawer"}
                ),
                Div(
                    H3("Add New Collection", cls="text-lg font-bold flex justify-center"),
                    Form(
                        Div(
                            Div(
                                Label("Collection Name:", cls="label"),
                                Input(
                                    type="text",
                                    name="collectionname",
                                    placeholder="Enter collection name",
                                    cls="input input-bordered w-full"
                                ),
                                cls="mb-4"
                            ),
                            Div(
                                Label("Description:", cls="label"),
                                Textarea(
                                    name="collectionarray",
                                    placeholder="Enter description",
                                    cls="textarea textarea-bordered w-full"
                                ),
                                cls="mb-4"
                            ),
                            Div(
                                Button(
                                    "Add Collection",
                                    type="submit",
                                    hx_trigger="load",
                                    cls="btn bg-black btn-outline w-full"
                                ),
                                cls="mt-4",
                                hx_post='/create_collection',
                                hx_swap="none"
                            ),
                            cls="p-4"
                        ),
                        cls="bg-ghost rounded-lg"
                    ),
                    cls="menu text-base-content min-h-full w-80 p-4",
                style="background-color: #feb0ee;"
                ),
                cls="drawer-side"
            ),
            cls="drawer drawer-end"
        )
    )
 
 add_record = Div(
        Div(
            # Drawer input (toggle)
            Input(
                id="add-record-drawer",
                type="checkbox",
                cls="drawer-toggle"
            ),
            # Drawer content
            Div(
                
                cls="drawer-content"
            ),
            # Drawer sidebar (Form for adding collections)
            Div(
                Label(
                    cls="drawer-overlay",
                    **{"for": "add-record-drawer"}
                ),
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
                                Button(
                                    "Add Record",
                                    type="submit",
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
 
 def list_collection():
    database = db.fetch_keys()
    # Accumulate Div elements for each table
    cards = []
    for key in database:
        cards.append(
            Div(
                Div(key, cls="text-lg font-bold"),  # Table name
                Div(db.fetch(key)['value']['text'] if 'value' in db.fetch(key) else '', cls="text-md"),  # Column name
                cls="card w-48 mb-3 hover:bg-gray-50 bg-white border border-black hover:translate-x-1 hover:translate-y-1 shadow-md p-4 m-2"
            )
        )
    # Return all cards wrapped in a parent Div
    return Div(*cards, cls="overflow-x-auto")

 
 collections = Div(
                            # Card container
                            Div(
                                # Card 1
                            Div(
                             Div("Collections", cls="text-lg font-bold w-48"),  # Table name
                                ),
                                list_collection(),
                                cls="flex flex-col gap-4"  # Container for cards with spacing between them
                            ),
                            cls="overflow-x-auto p-4"  # Wrapper with padding and horizontal scrolling
                        )

 records = Div(
                           Table(
                                    # Table head
                                    Thead(
                                        Tr(
                                            Th("No.", cls="text-center px-4 py-2"),
                                            Th("Name", cls="text-left px-4 py-2"),
                                            Th("Job", cls="text-left px-4 py-2"),
                                            Th("Favorite Color", cls="text-left px-4 py-2"),
                                            cls="bg-gray-50"
                                        )
                                    ),
                                    # Table body
                                    Tbody(
                                        # Row 1
                                        Tr(
                                            Th("1", cls="text-center px-4 py-2"),
                                            Td("Cy Ganderton", cls="px-4 py-2"),
                                            Td("Quality Control Specialist", cls="px-4 py-2"),
                                            Td("Blue", cls="px-4 py-2"),
                                            cls="border hover:bg-gray-100"
                                        )
                                    ),
                                    cls="table-auto w-full bg-white border border-black"
                                ),
                                Label(
                    "Add record",
                    cls="btn bg-black btn-outline w-64 mt-5",
                    **{"for": "add-record-drawer"}
                    ),
                                cls="card bg-ghost rounded-box flex-grow place-items-center overflow-x-auto")

 return (
        # Header with styles and scripts
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
        # Navbar
        Head(
            Div(
                Div("DaisyUI", cls="text-xl font-bold"),
                cls="navbar bg-base-300",
                style="background-color: #feb0ee;"
            )
        ),
        # Main Body with drawer
        Body(
            Div(
               # Main content (Collection list and records)
                Div(
                    Div(
                       Div(I(cls="ti ti-database text-2xl"), " Database", cls="text-2xl font-bold"),
                        # Collections and records
                        Div(
                            collections,
                            Div(cls="divider divider-horizontal"),
                            records,
                            cls="flex w-full max-w-6xl h-80"
                        ),
                        Label(
                    "Add collection",
                    cls="btn bg-black btn-outline w-48",
                    **{"for": "add-collection-drawer"}
                    ),
                        cls="card-body"
                    ),
                    cls="card shadow-xl mx-auto w-full max-w-6xl",
                    style="background-color: #feb0ee;"
                ),
                add_collection,
                add_record,
                cls="container mx-auto py-6 px-4"
            ),
            data_theme="light",
            style="min-height:100vh;"
        )
    )



@rt('/create_collection')
def post(collectionname:str,collectionarray:str):
    db.create(collectionname,{'text': f'{collectionarray}'})

serve()


