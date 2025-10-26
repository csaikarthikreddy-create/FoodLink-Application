import reflex as rx
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str
    full_name: str
    phone: str
    events: list["Event"] = Relationship(back_populates="organizer")
    ngo: Optional["NGO"] = Relationship(back_populates="user")


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organizer_id: int = Field(foreign_key="user.id")
    name: str
    location_address: str
    latitude: float
    longitude: float
    event_date: str
    event_time: str
    expected_surplus_kg: float
    surplus_description: str
    status: str
    organizer: User = Relationship(back_populates="events")
    notifications: list["NGONotification"] = Relationship(back_populates="event")


class NGO(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    organization_name: str
    location_address: str
    latitude: float
    longitude: float
    service_area_radius_miles: int
    user: User = Relationship(back_populates="ngo")
    notification_preferences: list["NGONotificationPreferences"] = Relationship(
        back_populates="ngo"
    )
    notifications: list["NGONotification"] = Relationship(back_populates="ngo")


class NGONotificationPreferences(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ngo_id: int = Field(foreign_key="ngo.id")
    channel: str
    contact_info: str
    enabled: bool = True
    ngo: NGO = Relationship(back_populates="notification_preferences")


class NGONotification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ngo_id: int = Field(foreign_key="ngo.id")
    event_id: int = Field(foreign_key="event.id")
    channel: str
    status: str
    created_at: str
    error_message: Optional[str] = Field(default=None)
    ngo: NGO = Relationship(back_populates="notifications")
    event: Event = Relationship(back_populates="notifications")