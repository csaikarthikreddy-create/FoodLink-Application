import reflex as rx
from app.states.auth_state import AuthState


def auth_form_input(label: str, name: str, type: str, placeholder: str) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.input(
            name=name,
            type=type,
            placeholder=placeholder,
            required=True,
            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
        ),
        class_name="mb-4",
    )


def login_form() -> rx.Component:
    return rx.el.form(
        rx.el.h2(
            "Sign in to your account",
            class_name="text-2xl font-bold text-center text-gray-800",
        ),
        auth_form_input("Email", "email", "email", "you@example.com"),
        auth_form_input("Password", "password", "password", "••••••••"),
        rx.el.button(
            "Sign In",
            type="submit",
            class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
        ),
        on_submit=AuthState.login,
        class_name="space-y-6",
    )


def register_form() -> rx.Component:
    return rx.el.form(
        rx.el.h2(
            "Create a new account",
            class_name="text-2xl font-bold text-center text-gray-800",
        ),
        rx.cond(
            AuthState.form_role == "organizer",
            auth_form_input("Full Name", "full_name", "text", "John Doe"),
            auth_form_input(
                "Organization Name", "organization_name", "text", "e.g. Happy Shelter"
            ),
        ),
        auth_form_input("Email", "email", "email", "you@example.com"),
        auth_form_input("Phone", "phone", "tel", "123-456-7890"),
        auth_form_input("Password", "password", "password", "••••••••"),
        auth_form_input("Confirm Password", "confirm_password", "password", "••••••••"),
        rx.el.div(
            rx.el.label("I am a...", class_name="text-sm font-medium text-gray-700"),
            rx.el.select(
                rx.el.option("Event Organizer", value="organizer"),
                rx.el.option("NGO", value="ngo"),
                name="role",
                value=AuthState.form_role,
                on_change=AuthState.set_form_role,
                class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md",
            ),
            class_name="mb-4",
        ),
        rx.el.button(
            "Create Account",
            type="submit",
            class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
        ),
        on_submit=AuthState.register,
        class_name="space-y-6",
    )


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("sprout", class_name="h-12 w-12 mx-auto text-blue-600"),
                rx.el.h1(
                    "FoodLink",
                    class_name="mt-2 text-center text-3xl font-extrabold text-gray-900",
                ),
                class_name="mb-8",
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    AuthState.error_message,
                    class_name="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md relative mb-6",
                    role="alert",
                ),
                None,
            ),
            rx.cond(AuthState.show_login, login_form(), register_form()),
            rx.el.p(
                rx.el.button(
                    rx.cond(
                        AuthState.show_login,
                        "Don't have an account? Sign Up",
                        "Already have an account? Sign In",
                    ),
                    on_click=AuthState.toggle_form,
                    class_name="font-medium text-blue-600 hover:text-blue-500",
                ),
                class_name="mt-6 text-center text-sm text-gray-600",
            ),
            class_name="w-full max-w-md p-8 space-y-8 bg-white shadow-lg rounded-xl",
        ),
        class_name="min-h-screen bg-gray-50 flex flex-col justify-center items-center py-12 sm:px-6 lg:px-8 font-['Raleway']",
    )