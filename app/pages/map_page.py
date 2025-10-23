import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import latlng
from app.states.map_state import MapState
from app.components.sidebar import sidebar
from app.components.header import header


def event_marker(event: dict) -> rx.Component:
    return rxe.map.marker(
        rxe.map.popup(
            rx.el.div(
                rx.el.h3(event["name"], class_name="font-bold"),
                rx.el.p(f"Status: {event['status']}"),
            )
        ),
        position=latlng(lat=event["latitude"], lng=event["longitude"]),
        icon={"iconUrl": "/event_marker.png", "iconSize": [32, 32]},
    )


def ngo_marker(ngo: dict) -> rx.Component:
    return rxe.map.marker(
        rxe.map.popup(
            rx.el.div(rx.el.h3(ngo["organization_name"], class_name="font-bold"))
        ),
        position=latlng(lat=ngo["latitude"], lng=ngo["longitude"]),
        icon={"iconUrl": "/ngo_marker.png", "iconSize": [32, 32]},
    )


def map_view() -> rx.Component:
    return rxe.map(
        rxe.map.tile_layer(
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        ),
        rx.foreach(MapState.events, event_marker),
        rx.foreach(MapState.ngos, ngo_marker),
        id="foodlink-map",
        center=MapState.center,
        zoom=MapState.zoom,
        height="100%",
        width="100%",
        class_name="rounded-lg shadow-md",
    )


def map_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Events and NGOs Map",
                        class_name="text-3xl font-bold text-gray-800 mb-4",
                    ),
                    rx.el.div(map_view(), class_name="h-[70vh] w-full"),
                    class_name="p-6",
                )
            ),
            class_name="flex-1 flex flex-col",
        ),
        on_mount=MapState.load_map_data,
        class_name="flex min-h-screen bg-gray-50 font-['Raleway']",
    )