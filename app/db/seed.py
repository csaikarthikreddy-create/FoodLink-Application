import reflex as rx
import bcrypt
from sqlmodel import delete, SQLModel
from app.db.base import User, Event, NGO, NGONotification, NGONotificationPreferences


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def main():
    engine = rx.model.get_engine()
    SQLModel.metadata.create_all(engine)
    with rx.session() as session:
        session.exec(delete(NGONotification))
        session.exec(delete(NGONotificationPreferences))
        session.exec(delete(Event))
        session.exec(delete(NGO))
        session.exec(delete(User))
        session.commit()
        organizer1 = User(
            email="john@events.com",
            password_hash=hash_password("password123"),
            role="organizer",
            full_name="John Smith",
            phone="111-222-3333",
        )
        organizer2 = User(
            email="sarah@events.com",
            password_hash=hash_password("password123"),
            role="organizer",
            full_name="Sarah Johnson",
            phone="444-555-6666",
        )
        session.add(organizer1)
        session.add(organizer2)
        session.commit()
        session.refresh(organizer1)
        session.refresh(organizer2)
        ngo_user1 = User(
            email="contact@hopeshelter.org",
            password_hash=hash_password("password123"),
            role="ngo",
            full_name="Hope Shelter Contact",
            phone="777-888-9999",
        )
        session.add(ngo_user1)
        session.commit()
        session.refresh(ngo_user1)
        ngo1 = NGO(
            user_id=ngo_user1.id,
            organization_name="Hope Shelter",
            location_address="Downtown LA",
            latitude=34.0522,
            longitude=-118.2437,
            service_area_radius_miles=10,
        )
        ngo_user2 = User(
            email="info@gracehome.org",
            password_hash=hash_password("password123"),
            role="ngo",
            full_name="Grace Old Age Home Contact",
            phone="123-456-7890",
        )
        session.add(ngo_user2)
        session.commit()
        session.refresh(ngo_user2)
        ngo2 = NGO(
            user_id=ngo_user2.id,
            organization_name="Grace Old Age Home",
            location_address="Pasadena",
            latitude=34.1478,
            longitude=-118.1445,
            service_area_radius_miles=15,
        )
        ngo_user3 = User(
            email="admin@sunriseorphanage.com",
            password_hash=hash_password("password123"),
            role="ngo",
            full_name="Sunrise Orphanage Contact",
            phone="987-654-3210",
        )
        session.add(ngo_user3)
        session.commit()
        session.refresh(ngo_user3)
        ngo3 = NGO(
            user_id=ngo_user3.id,
            organization_name="Sunrise Orphanage",
            location_address="Santa Monica",
            latitude=34.0195,
            longitude=-118.4912,
            service_area_radius_miles=12,
        )
        session.add(ngo1)
        session.add(ngo2)
        session.add(ngo3)
        session.commit()
        event1 = Event(
            organizer_id=organizer1.id,
            name="Annual Charity Gala",
            location_address="LA Convention Center",
            latitude=34.0403,
            longitude=-118.2699,
            event_date="2024-11-15",
            event_time="18:00",
            expected_surplus_kg=100,
            surplus_description="Mixed catering",
            status="Surplus Available",
        )
        event2 = Event(
            organizer_id=organizer1.id,
            name="Tech Conference 2024",
            location_address="Pasadena Convention Center",
            latitude=34.1448,
            longitude=-118.142,
            event_date="2024-12-01",
            event_time="09:00",
            expected_surplus_kg=75,
            surplus_description="Sandwiches and salads",
            status="Scheduled",
        )
        event3 = Event(
            organizer_id=organizer2.id,
            name="Wedding Reception",
            location_address="Santa Monica Beach Club",
            latitude=34.0094,
            longitude=-118.4911,
            event_date="2024-11-20",
            event_time="19:00",
            expected_surplus_kg=50,
            surplus_description="Buffet style dinner",
            status="Surplus Available",
        )
        event4 = Event(
            organizer_id=organizer2.id,
            name="Community Festival",
            location_address="Griffith Park",
            latitude=34.1366,
            longitude=-118.2944,
            event_date="2024-11-22",
            event_time="12:00",
            expected_surplus_kg=120,
            surplus_description="BBQ and sides",
            status="Surplus Available",
        )
        event5 = Event(
            organizer_id=organizer1.id,
            name="Corporate Offsite",
            location_address="Long Beach",
            latitude=33.7701,
            longitude=-118.1937,
            event_date="2024-12-10",
            event_time="10:00",
            expected_surplus_kg=40,
            surplus_description="Breakfast and lunch boxes",
            status="Scheduled",
        )
        session.add_all([event1, event2, event3, event4, event5])
        session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    main()