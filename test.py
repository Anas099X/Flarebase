from fasthtml.common import *
from urllib.parse import parse_qs

app = FastHTML(exts="ws")
rt = app.route

@rt("/")
def get():
    """
    Renders the main page with dynamic input fields and a submit button.
    """
    return (
        # Main Page
        Body(
            Div(
                H3("Dynamic Input Test", cls="text-lg font-bold mb-4"),
                # Input fields container
                Div(
                    Input(type="text", name="field_1e", placeholder="Field 1", cls="input input-bordered w-full mb-2"),
                    Input(type="text", name="field_2d", placeholder="Field 2", cls="input input-bordered w-full mb-2"),
                    Input(type="text", name="field_3v", placeholder="Field 3", cls="input input-bordered w-full mb-2"),
                    Input(type="text", name="field_4a", placeholder="Field 3", cls="input input-bordered w-full mb-2"),
                    Input(type="text", name="field_3dc", placeholder="Field 3", cls="input input-bordered w-full mb-2"),
                    Input(type="text", name="field_3dc4", placeholder="Field 3", cls="input input-bordered w-full mb-2"),
                    Input(type="text", name="field_3d4", placeholder="Field 3", cls="input input-bordered w-full mb-2"),
                    id="fields",  # Container for dynamic inputs
                ),
                # Submit button
                Button(
                    "Submit Inputs",
                    hx_post="/process-fields",  # HTMX request to backend
                    hx_target="#results",  # Updates the #results div
                    hx_include="#fields input",  # Includes all inputs in the #fields div
                    hx_swap="innerHTML",
                    cls="btn btn-primary mt-4"
                ),
                # Results section
                Div(
                    "Your submitted data will appear here.",
                    id="results",
                    cls="mt-6 text-gray-500"
                ),
                cls="container mx-auto p-6"
            ),
            data_theme="light",
            style="min-height:100vh;"
        )
    )

@rt("/process-fields")
async def post(request):
    """
    Processes the submitted inputs and returns them as a list.
    """
    # Parse the form data sent by HTMX
    body = await request.body()  # Get the raw body of the request
    # Generate a list of submitted values
    result = [
        Li(f"{value[1][0]}", cls="text-green-500")
        for value in  parse_qs(body.decode()).items()
    ]
    print(list(parse_qs(body.decode()).items())[0][1][0])
    # Return the formatted result
    return Ul(
        H3("Submitted Data:", cls="text-lg font-bold mb-2"),
        *result,
        cls="list-disc list-inside"
    )

serve()
