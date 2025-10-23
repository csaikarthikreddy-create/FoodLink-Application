import reflex as rx
from reflex_enterprise.components.map.types import LatLng, latlng
from sqlmodel import text
import logging


class MapState(rx.State):
    center: LatLng = latlng(lat=34.0522, lng=-118.2437)
    zoom: float = 10.0
    events: list[dict] = []
    ngos: list[dict] = []

    @rx.event
    def load_map_data(self):
        try:
            with rx.session() as session:
                event_results = session.exec(
                    text(
                        "SELECT id, name, latitude, longitude, status FROM event WHERE status = 'Surplus Available'"
                    )
                ).all()
                self.events = [dict(row._mapping) for row in event_results]
                ngo_results = session.exec(
                    text("SELECT id, organization_name, latitude, longitude FROM ngo")
                ).all()
                self.ngos = [dict(row._mapping) for row in ngo_results]
        except Exception as e:
            logging.exception(f"Error loading map data: {e}")