import reflex as rx
from app.states.organizer_state import OrganizerState
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.event_form import event_form_modal


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Scheduled",
                "bg-blue-100 text-blue-800 px-2 py-1 text-xs font-medium rounded-full",
            ),
            (
                "Completed",
                "bg-gray-100 text-gray-800 px-2 py-1 text-xs font-medium rounded-full",
            ),
            (
                "Surplus Available",
                "bg-yellow-100 text-yellow-800 px-2 py-1 text-xs font-medium rounded-full",
            ),
            (
                "Distributed",
                "bg-green-100 text-green-800 px-2 py-1 text-xs font-medium rounded-full",
            ),
            "bg-gray-100 text-gray-800 px-2 py-1 text-xs font-medium rounded-full",
        ),
    )


def event_card(event: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(event["name"], class_name="text-lg font-semibold text-gray-800"),
            status_badge(event["status"]),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(event["location_address"], class_name="text-sm text-gray-600 mt-1"),
        rx.el.p(
            f"Date: {event['event_date']}", class_name="text-sm text-gray-600 mt-1"
        ),
        rx.el.div(
            rx.el.button(
                "Edit",
                class_name="text-sm font-medium text-blue-600 hover:text-blue-800",
            ),
            rx.el.button(
                "Mark Surplus",
                on_click=lambda: OrganizerState.set_status(
                    event["id"], "Surplus Available"
                ),
                class_name="text-sm font-medium text-orange-600 hover:text-orange-800",
            ),
            rx.el.button(
                "Delete",
                class_name="text-sm font-medium text-red-600 hover:text-red-800",
            ),
            class_name="flex gap-4 mt-4",
        ),
        class_name="bg-white p-4 rounded-lg shadow-sm border border-gray-200",
    )


def organizer_dashboard() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Dashboard", class_name="text-3xl font-bold text-gray-800"
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="mr-2 h-5 w-5"),
                            "Create Event",
                            on_click=OrganizerState.toggle_create_modal,
                            class_name="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg shadow-sm hover:bg-blue-700",
                        ),
                        class_name="flex justify-between items-center",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Total Events",
                                class_name="text-sm font-medium text-gray-500",
                            ),
                            rx.el.p(
                                OrganizerState.events.length(),
                                class_name="mt-1 text-3xl font-semibold text-gray-900",
                            ),
                            class_name="bg-white p-6 rounded-lg shadow",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Surplus Available",
                                class_name="text-sm font-medium text-gray-500",
                            ),
                            rx.el.p(
                                "0",
                                class_name="mt-1 text-3xl font-semibold text-gray-900",
                            ),
                            class_name="bg-white p-6 rounded-lg shadow",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Food Distributed",
                                class_name="text-sm font-medium text-gray-500",
                            ),
                            rx.el.p(
                                "0 kg",
                                class_name="mt-1 text-3xl font-semibold text-gray-900",
                            ),
                            class_name="bg-white p-6 rounded-lg shadow",
                        ),
                        class_name="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "My Events",
                            class_name="text-2xl font-bold text-gray-800 mt-8 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(OrganizerState.events, event_card),
                            class_name="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6",
                        ),
                    ),
                    class_name="p-6",
                )
            ),
            event_form_modal(),
            class_name="flex-1 flex flex-col",
        ),
        on_mount=OrganizerState.check_auth_and_load,
        class_name="flex min-h-screen bg-gray-50 font-['Raleway']",
    )