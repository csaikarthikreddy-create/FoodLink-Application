import reflex as rx
from app.states.auth_state import AuthState
from app.states.ngo_state import NGOState


def ngo_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("sprout", class_name="h-8 w-8 text-blue-600"),
                rx.cond(
                    ~NGOState.sidebar_collapsed,
                    rx.el.h1("FoodLink", class_name="text-2xl font-bold ml-2"),
                    None,
                ),
                class_name="flex items-center p-4 border-b border-gray-200",
            ),
            rx.el.nav(
                rx.el.a(
                    rx.icon("layout-dashboard", class_name="h-5 w-5"),
                    rx.cond(
                        ~NGOState.sidebar_collapsed,
                        rx.el.span("Dashboard", class_name="ml-3"),
                        None,
                    ),
                    href="#",
                    class_name="flex items-center px-3 py-2 text-white bg-blue-600 rounded-lg",
                ),
                rx.el.a(
                    rx.icon("map", class_name="h-5 w-5"),
                    rx.cond(
                        ~NGOState.sidebar_collapsed,
                        rx.el.span("Map View", class_name="ml-3"),
                        None,
                    ),
                    href="/map",
                    class_name="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                rx.el.a(
                    rx.icon("bell", class_name="h-5 w-5"),
                    rx.cond(
                        ~NGOState.sidebar_collapsed,
                        rx.el.span("Notifications", class_name="ml-3"),
                        None,
                    ),
                    href="#",
                    class_name="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                rx.el.a(
                    rx.icon("user", class_name="h-5 w-5"),
                    rx.cond(
                        ~NGOState.sidebar_collapsed,
                        rx.el.span("Profile", class_name="ml-3"),
                        None,
                    ),
                    href="#",
                    class_name="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                class_name="flex-1 space-y-2 p-4",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=rx.cond(
            NGOState.sidebar_collapsed,
            "bg-white border-r border-gray-200 w-20 transition-all",
            "bg-white border-r border-gray-200 w-64 transition-all",
        ),
    )


def ngo_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", class_name="h-6 w-6"),
                on_click=NGOState.toggle_sidebar,
                class_name="p-2 rounded-md hover:bg-gray-100",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.p(f"Welcome, {AuthState.current_user_name}"),
            rx.el.button(
                "Logout",
                on_click=AuthState.logout,
                class_name="ml-4 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
            ),
            class_name="flex items-center",
        ),
        class_name="flex items-center justify-between p-4 border-b border-gray-200 bg-white",
    )


def surplus_event_card(event: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(event["name"], class_name="text-lg font-semibold text-gray-800"),
            rx.el.span(
                f"{event['distance']} miles away",
                class_name="bg-blue-100 text-blue-800 px-2 py-1 text-xs font-medium rounded-full",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(
            f"Location: {event['location_address']}",
            class_name="text-sm text-gray-600 mt-2",
        ),
        rx.el.p(
            f"Surplus: {event['expected_surplus_kg']} kg of {event['surplus_description']}",
            class_name="text-sm text-gray-600 mt-1",
        ),
        rx.el.div(
            rx.el.p(
                f"Organizer: {event['organizer_name']}",
                class_name="text-sm font-medium",
            ),
            rx.el.p(
                f"Contact: {event['organizer_phone']}", class_name="text-sm font-medium"
            ),
            class_name="mt-4 pt-4 border-t border-gray-200 flex justify-between items-center",
        ),
        class_name="bg-white p-4 rounded-lg shadow-sm border border-gray-200",
    )


def ngo_dashboard() -> rx.Component:
    return rx.el.div(
        ngo_sidebar(),
        rx.el.div(
            ngo_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Nearby Surplus Food",
                        class_name="text-3xl font-bold text-gray-800",
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
        on_mount=NGOState.check_auth_and_load,
        class_name="flex min-h-screen bg-gray-50 font-['Raleway']",
    )