import reflex as rx
from sqlmodel import text
import logging
from app.states.ngo_state import haversine
import datetime
from app.services.notification_service import NotificationService


class NotificationsState(rx.State):
    @rx.event
    def trigger_notifications(self, event_id: int):
        logging.info(f"Triggering notifications for event_id: {event_id}")
        notification_service = NotificationService()
        with rx.session() as session:
            try:
                event_res = session.exec(
                    text("""SELECT e.*, u.full_name as organizer_name, u.phone as organizer_phone
                           FROM event e JOIN user u ON e.organizer_id = u.id
                           WHERE e.id = :event_id""").bindparams(event_id=event_id)
                ).first()
                if not event_res:
                    logging.error(f"Event with id {event_id} not found.")
                    return
                event_data = dict(event_res._mapping)
                event_lat, event_lon = (event_data["latitude"], event_data["longitude"])
                ngo_results = session.exec(
                    text("""SELECT n.id, n.latitude, n.longitude, n.service_area_radius_miles, np.channel, np.contact_info
                           FROM ngo n JOIN ngonotificationpreferences np ON n.id = np.ngo_id
                           WHERE np.enabled = TRUE""")
                ).all()
                nearby_ngos = []
                for ngo in ngo_results:
                    distance = haversine(
                        event_lat, event_lon, ngo.latitude, ngo.longitude
                    )
                    if distance <= ngo.service_area_radius_miles:
                        ngo_data = dict(ngo._mapping)
                        ngo_data["distance"] = distance
                        nearby_ngos.append(ngo_data)
                logging.info(
                    f"Found {len(nearby_ngos)} nearby NGOs for event {event_id}."
                )
                for ngo_data in nearby_ngos:
                    status = "sent"
                    error_message = None
                    try:
                        notification_service.send_notification(
                            channel=ngo_data["channel"],
                            recipient=ngo_data["contact_info"],
                            event_data=event_data,
                            ngo_data=ngo_data,
                        )
                        logging.info(
                            f"Successfully sent {ngo_data['channel']} notification to NGO {ngo_data['id']}."
                        )
                    except Exception as e:
                        status = "failed"
                        error_message = str(e)
                        logging.exception(
                            f"Failed to send {ngo_data['channel']} notification to NGO {ngo_data['id']}: {e}"
                        )
                    session.exec(
                        text("""INSERT INTO ngonotification (ngo_id, event_id, channel, status, created_at, error_message)
                               VALUES (:ngo_id, :event_id, :channel, :status, :created_at, :error_message)""").bindparams(
                            ngo_id=ngo_data["id"],
                            event_id=event_id,
                            channel=ngo_data["channel"],
                            status=status,
                            created_at=str(datetime.datetime.utcnow()),
                            error_message=error_message,
                        )
                    )
                session.commit()
            except Exception as e:
                logging.exception(f"Error triggering notifications: {e}")
                session.rollback()