import reflex as rx
from app.db.models import Event, NGO, User
from app.states.auth_state import AuthState
from sqlmodel import text
import math
import logging


def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = (
        math.sin(dLat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


class NGOState(rx.State):
    ngo_profile: NGO | None = None
    available_events: list[dict] = []
    sidebar_collapsed: bool = False
    notifications: list[dict] = []
    unread_notifications: int = 0

    @rx.event
    async def check_auth_and_load(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or auth_state.current_user_role != "ngo":
            yield rx.redirect("/login")
            return
        yield NGOState.load_ngo_profile
        yield NGOState.load_available_events
        yield NGOState.load_notifications

    @rx.event
    async def load_ngo_profile(self):
        auth_state = await self.get_state(AuthState)
        if auth_state.current_user_id:
            try:
                with rx.session() as session:
                    result = session.exec(
                        text("SELECT * FROM ngo WHERE user_id = :user_id").bindparams(
                            user_id=auth_state.current_user_id
                        )
                    ).first()
                    if result:
                        self.ngo_profile = dict(result._mapping)
            except Exception as e:
                logging.exception(f"Error loading NGO profile: {e}")
                self.ngo_profile = None

    @rx.event
    async def load_available_events(self):
        if not self.ngo_profile:
            self.available_events = []
            return
        ngo_lat = self.ngo_profile["latitude"]
        ngo_lon = self.ngo_profile["longitude"]
        radius = self.ngo_profile["service_area_radius_miles"]
        try:
            with rx.session() as session:
                all_surplus_events_rows = session.exec(
                    text("""SELECT event.*, user.full_name as organizer_name, user.phone as organizer_phone
                           FROM event JOIN user ON event.organizer_id = user.id 
                           WHERE event.status = 'Surplus Available'""")
                ).all()
            nearby_events = []
            for row in all_surplus_events_rows:
                event = dict(row._mapping)
                distance = haversine(
                    ngo_lat, ngo_lon, event["latitude"], event["longitude"]
                )
                if distance <= radius:
                    event_with_dist = {**event, "distance": round(distance, 2)}
                    nearby_events.append(event_with_dist)
            self.available_events = sorted(nearby_events, key=lambda x: x["distance"])
        except Exception as e:
            logging.exception(f"Error loading available events: {e}")
            self.available_events = []

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_collapsed = not self.sidebar_collapsed

    @rx.event
    def load_test_data(self):
        """Load data for a specific NGO for testing purposes."""
        try:
            with rx.session() as session:
                result = session.exec(
                    text("SELECT * FROM ngo WHERE id = :ngo_id").bindparams(ngo_id=1)
                ).first()
                if result:
                    self.ngo_profile = dict(result._mapping)
                else:
                    self.ngo_profile = None
                    self.available_events = []
                    return
            ngo_lat = self.ngo_profile["latitude"]
            ngo_lon = self.ngo_profile["longitude"]
            radius = self.ngo_profile["service_area_radius_miles"]
            with rx.session() as session:
                all_surplus_events_rows = session.exec(
                    text("""SELECT event.*, user.full_name as organizer_name, user.phone as organizer_phone
                           FROM event JOIN user ON event.organizer_id = user.id 
                           WHERE event.status = 'Surplus Available'""")
                ).all()
            nearby_events = []
            for row in all_surplus_events_rows:
                event = dict(row._mapping)
                distance = haversine(
                    ngo_lat, ngo_lon, event["latitude"], event["longitude"]
                )
                if distance <= radius:
                    event_with_dist = {**event, "distance": round(distance, 2)}
                    nearby_events.append(event_with_dist)
            self.available_events = sorted(nearby_events, key=lambda x: x["distance"])
        except Exception as e:
            logging.exception(f"Error loading test data: {e}")
            self.available_events = []

    @rx.event
    async def load_notifications(self):
        auth_state = await self.get_state(AuthState)
        if self.ngo_profile:
            try:
                with rx.session() as session:
                    query = text("""SELECT n.id, n.event_id, n.channel, n.status, n.created_at, e.name as event_name, e.location_address
                                   FROM ngonotification n
                                   JOIN event e ON n.event_id = e.id
                                   WHERE n.ngo_id = :ngo_id
                                   ORDER BY n.created_at DESC""")
                    result = session.exec(
                        query.bindparams(ngo_id=self.ngo_profile["id"])
                    ).all()
                    self.notifications = [dict(row._mapping) for row in result]
                    self.unread_notifications = sum(
                        (1 for n in self.notifications if n["status"] == "sent")
                    )
            except Exception as e:
                logging.exception(f"Error loading notifications: {e}")