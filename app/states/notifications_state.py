import reflex as rx
from sqlmodel import text
import logging
from app.states.ngo_state import haversine
import datetime


class NotificationsState(rx.State):
    @rx.event
    def trigger_notifications(self, event_id: int):
        logging.info(f"Triggering notifications for event_id: {event_id}")
        with rx.session() as session:
            try:
                event_res = session.exec(
                    text(
                        "SELECT latitude, longitude FROM event WHERE id = :event_id"
                    ).bindparams(event_id=event_id)
                ).first()
                if not event_res:
                    logging.error(f"Event with id {event_id} not found.")
                    return
                event_lat, event_lon = (event_res.latitude, event_res.longitude)
                ngo_results = session.exec(
                    text(
                        "SELECT id, latitude, longitude, service_area_radius_miles FROM ngo"
                    )
                ).all()
                nearby_ngos = []
                for ngo in ngo_results:
                    distance = haversine(
                        event_lat, event_lon, ngo.latitude, ngo.longitude
                    )
                    if distance <= ngo.service_area_radius_miles:
                        nearby_ngos.append(ngo.id)
                logging.info(
                    f"Found {len(nearby_ngos)} nearby NGOs for event {event_id}."
                )
                for ngo_id in nearby_ngos:
                    logging.info(
                        f"Mock notification to NGO {ngo_id} for event {event_id} via preferred channel."
                    )
                    session.exec(
                        text("""INSERT INTO ngonotification (ngo_id, event_id, channel, status, created_at)
                               VALUES (:ngo_id, :event_id, :channel, :status, :created_at)""").bindparams(
                            ngo_id=ngo_id,
                            event_id=event_id,
                            channel="log",
                            status="sent",
                            created_at=str(datetime.datetime.utcnow()),
                        )
                    )
                session.commit()
            except Exception as e:
                logging.exception(f"Error triggering notifications: {e}")
                session.rollback()