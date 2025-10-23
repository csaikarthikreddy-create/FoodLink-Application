from typing import TypedDict


class User(TypedDict):
    id: int
    email: str
    password_hash: str
    role: str
    full_name: str
    phone: str


class Event(TypedDict):
    id: int
    organizer_id: int
    name: str
    location_address: str
    latitude: float
    longitude: float
    event_date: str
    event_time: str
    expected_surplus_kg: float
    surplus_description: str
    status: str


class NGO(TypedDict):
    id: int
    user_id: int
    organization_name: str
    location_address: str
    latitude: float
    longitude: float
    service_area_radius_miles: int


class NGONotificationPreferences(TypedDict):
    id: int
    ngo_id: int
    channel: str
    contact_info: str
    enabled: bool


class NGONotification(TypedDict):
    id: int
    ngo_id: int
    event_id: int
    channel: str
    status: str
    created_at: str