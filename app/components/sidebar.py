import reflex as rx
from app.states.organizer_state import OrganizerState


def nav_item(icon: str, text: str, href: str, is_active: bool) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.cond(
            ~OrganizerState.sidebar_collapsed, rx.el.span(text, class_name="ml-3"), None
        ),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center px-3 py-2 text-white bg-blue-600 rounded-lg",
            "flex items-center px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("sprout", class_name="h-8 w-8 text-blue-600"),
                rx.cond(
                    ~OrganizerState.sidebar_collapsed,
                    rx.el.h1("FoodLink", class_name="text-2xl font-bold ml-2"),
                    None,
                ),
                class_name="flex items-center p-4 border-b border-gray-200",
            ),
            rx.el.nav(
                nav_item("layout-dashboard", "Dashboard", "/", True),
                nav_item("calendar-days", "My Events", "#", False),
                nav_item("circle_plus", "Create Event", "#", False),
                nav_item("user", "Profile", "#", False),
                class_name="flex-1 space-y-2 p-4",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=rx.cond(
            OrganizerState.sidebar_collapsed,
            "bg-white border-r border-gray-200 w-20 transition-all",
            "bg-white border-r border-gray-200 w-64 transition-all",
        ),
    )