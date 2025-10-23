import reflex as rx
from app.states.organizer_state import OrganizerState


def form_input(
    label: str, name: str, type: str, placeholder: str, required: bool = True
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            name=name,
            type=type,
            placeholder=placeholder,
            required=required,
            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
        ),
        class_name="mb-4",
    )


def event_form_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 z-50 bg-black bg-opacity-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "Create New Event",
                            class_name="text-2xl font-bold text-gray-800",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="h-5 w-5"),
                                class_name="p-1 rounded-full hover:bg-gray-200",
                            )
                        ),
                        class_name="flex justify-between items-center pb-4 border-b",
                    ),
                    rx.el.form(
                        rx.el.div(
                            form_input(
                                "Event Name",
                                "name",
                                "text",
                                "e.g., Annual Charity Gala",
                            ),
                            form_input(
                                "Location Address",
                                "location_address",
                                "text",
                                "123 Main St, Anytown, USA",
                            ),
                            rx.el.div(
                                form_input(
                                    "Latitude",
                                    "latitude",
                                    "number",
                                    "e.g., 34.0522",
                                    required=True,
                                ),
                                form_input(
                                    "Longitude",
                                    "longitude",
                                    "number",
                                    "e.g., -118.2437",
                                    required=True,
                                ),
                                class_name="grid grid-cols-2 gap-4",
                            ),
                            rx.el.div(
                                form_input("Event Date", "event_date", "date", ""),
                                form_input("Event Time", "event_time", "time", ""),
                                class_name="grid grid-cols-2 gap-4",
                            ),
                            form_input(
                                "Expected Surplus (kg)",
                                "expected_surplus_kg",
                                "number",
                                "e.g., 50",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Surplus Description",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.textarea(
                                    name="surplus_description",
                                    placeholder="Describe the type of food (e.g., vegetarian, non-veg, bakery items)",
                                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
                                ),
                                class_name="mb-4",
                            ),
                        ),
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Cancel",
                                    type="button",
                                    class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300",
                                )
                            ),
                            rx.el.button(
                                "Create Event",
                                type="submit",
                                class_name="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700",
                            ),
                            class_name="flex justify-end gap-4 pt-4 border-t",
                        ),
                        on_submit=OrganizerState.create_event,
                        reset_on_submit=True,
                        class_name="mt-4",
                    ),
                    class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-2xl",
                )
            ),
        ),
        open=OrganizerState.show_create_modal,
        on_open_change=OrganizerState.toggle_create_modal,
    )