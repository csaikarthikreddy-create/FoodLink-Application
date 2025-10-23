import reflex as rx
from app.states.auth_state import AuthState
from app.states.organizer_state import OrganizerState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", class_name="h-6 w-6"),
                on_click=OrganizerState.toggle_sidebar,
                class_name="p-2 rounded-md hover:bg-gray-100",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.el.div(
                        AuthState.initial,
                        class_name="flex items-center justify-center h-8 w-8 bg-blue-600 text-white rounded-full font-semibold",
                    ),
                    rx.el.p(AuthState.current_user_name, class_name="ml-2 font-medium"),
                    rx.icon("chevron-down", class_name="ml-1 h-4 w-4"),
                    class_name="flex items-center p-2 rounded-lg hover:bg-gray-100",
                )
            ),
            rx.el.button(
                "Logout",
                on_click=AuthState.logout,
                class_name="ml-4 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
            ),
            class_name="flex items-center",
        ),
        class_name="flex items-center justify-between p-4 border-b border-gray-200 bg-white",
    )