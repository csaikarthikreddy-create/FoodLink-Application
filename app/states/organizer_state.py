import reflex as rx
from app.db.models import Event
from app.states.auth_state import AuthState
from sqlmodel import text


class OrganizerState(rx.State):
    events: list[Event] = []
    sidebar_collapsed: bool = False
    show_create_modal: bool = False
    editing_event_id: int | None = None

    @rx.event
    async def check_auth_and_load(self):
        auth_state = await self.get_state(AuthState)
        if (
            not auth_state.is_authenticated
            or auth_state.current_user_role != "organizer"
        ):
            yield rx.redirect("/login")
            return
        yield OrganizerState.load_events

    @rx.event
    async def load_events(self):
        auth_state = await self.get_state(AuthState)
        if auth_state.current_user_id:
            with rx.session() as session:
                result = session.exec(
                    text(
                        "SELECT * FROM event WHERE organizer_id = :organizer_id"
                    ).bindparams(organizer_id=auth_state.current_user_id)
                ).all()
                self.events = [dict(row._mapping) for row in result]

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_collapsed = not self.sidebar_collapsed

    @rx.event
    def toggle_create_modal(self):
        self.show_create_modal = not self.show_create_modal
        self.editing_event_id = None

    @rx.event
    async def create_event(self, form_data: dict):
        auth_state = await self.get_state(AuthState)
        if auth_state.current_user_id:
            with rx.session() as session:
                query = text("""INSERT INTO event (organizer_id, name, location_address, latitude, longitude, 
                                       event_date, event_time, expected_surplus_kg, surplus_description, status)
                           VALUES (:organizer_id, :name, :location_address, :latitude, :longitude, 
                                   :event_date, :event_time, :expected_surplus_kg, :surplus_description, :status)
                           RETURNING id""")
                result = session.exec(
                    query.bindparams(
                        organizer_id=auth_state.current_user_id,
                        name=form_data["name"],
                        location_address=form_data["location_address"],
                        latitude=float(form_data["latitude"]),
                        longitude=float(form_data["longitude"]),
                        event_date=form_data["event_date"],
                        event_time=form_data["event_time"],
                        expected_surplus_kg=float(form_data["expected_surplus_kg"]),
                        surplus_description=form_data["surplus_description"],
                        status="Scheduled",
                    )
                ).first()
                session.commit()
            yield OrganizerState.toggle_create_modal
            yield OrganizerState.load_events

    @rx.event
    async def set_status(self, event_id: int, status: str):
        with rx.session() as session:
            session.exec(
                text(
                    "UPDATE event SET status = :status WHERE id = :event_id"
                ).bindparams(status=status, event_id=event_id)
            )
            session.commit()
        yield OrganizerState.load_events
        if status == "Surplus Available":
            from app.states.notifications_state import NotificationsState

            yield NotificationsState.trigger_notifications(event_id)