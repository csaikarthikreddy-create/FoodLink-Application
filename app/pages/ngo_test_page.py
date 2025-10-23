import reflex as rx
from app.states.ngo_state import NGOState
from app.pages.ngo_dashboard import ngo_sidebar, ngo_header, surplus_event_card


def ngo_test_page() -> rx.Component:
    """A test page to display the NGO dashboard without authentication."""
    return rx.el.div(
        ngo_sidebar(),
        rx.el.div(
            ngo_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Nearby Surplus Food (Test View)",
                            class_name="text-3xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            "This is a test view simulating the dashboard for 'Hope Shelter'.",
                            class_name="mt-2 p-2 bg-yellow-100 text-yellow-800 rounded-md text-sm",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.p(
                        "Events with available surplus food within your service area.",
                        class_name="text-gray-500 mt-1",
                    ),
                    rx.cond(
                        NGOState.available_events.length() > 0,
                        rx.el.div(
                            rx.foreach(NGOState.available_events, surplus_event_card),
                            class_name="mt-6 grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "No surplus food available nearby at the moment. We'll notify you when something comes up!"
                            ),
                            class_name="mt-6 text-center text-gray-500 bg-white p-8 rounded-lg shadow-sm",
                        ),
                    ),
                    class_name="p-6",
                )
            ),
            class_name="flex-1 flex flex-col",
        ),
        on_mount=NGOState.load_test_data,
        class_name="flex min-h-screen bg-gray-50 font-['Raleway']",
    )