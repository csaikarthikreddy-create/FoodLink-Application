import reflex_enterprise as rxe
import reflex as rx
from app.states.auth_state import AuthState
from app.pages.login_page import login_page
from app.pages.organizer_dashboard import organizer_dashboard
from app.pages.ngo_dashboard import ngo_dashboard
from app.pages.ngo_test_page import ngo_test_page
from app.pages.map_page import map_page


def index() -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated,
        rx.match(
            AuthState.current_user_role,
            ("organizer", organizer_dashboard()),
            ("ngo", ngo_dashboard()),
            login_page(),
        ),
        login_page(),
    )


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=",
            cross_origin="",
        ),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css",
        ),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(ngo_test_page, route="/ngo-test")
app.add_page(map_page, route="/map")