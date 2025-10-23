import reflex as rx
import bcrypt
from sqlmodel import text
from typing import Literal
from app.db.models import User


class AuthState(rx.State):
    is_authenticated: bool = False
    current_user_email: str = ""
    current_user_role: Literal["organizer", "ngo", ""] = ""
    current_user_name: str = ""
    current_user_id: int | None = None
    error_message: str = ""
    show_login: bool = True
    form_role: str = "organizer"

    @rx.event
    def toggle_form(self):
        self.show_login = not self.show_login
        self.error_message = ""
        self.form_role = "organizer"

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    @rx.event
    def register(self, form_data: dict):
        self.error_message = ""
        email = form_data.get("email")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        full_name = form_data.get("full_name", "")
        organization_name = form_data.get("organization_name", "")
        phone = form_data.get("phone")
        role = form_data.get("role")
        if role == "organizer":
            name_to_use = full_name
        else:
            name_to_use = organization_name
        if not all([email, password, confirm_password, name_to_use, phone, role]):
            self.error_message = "All fields are required."
            return
        if password != confirm_password:
            self.error_message = "Passwords do not match."
            return
        with rx.session() as session:
            existing_user = session.exec(
                text("SELECT * FROM user WHERE email = :email").bindparams(email=email)
            ).first()
            if existing_user:
                self.error_message = "User with this email already exists."
                return
            hashed_password = self._hash_password(password)
            user_insert_res = session.exec(
                text("""INSERT INTO user (email, password_hash, full_name, phone, role)
                       VALUES (:email, :password_hash, :full_name, :phone, :role) RETURNING id""").bindparams(
                    email=email,
                    password_hash=hashed_password,
                    full_name=name_to_use,
                    phone=phone,
                    role=role,
                )
            ).first()
            session.commit()
            if role == "ngo":
                user_id = user_insert_res.id
                session.exec(
                    text("""INSERT INTO ngo (user_id, organization_name, location_address, latitude, longitude, service_area_radius_miles)
                           VALUES (:user_id, :org_name, 'Default Address', 0, 0, 10)""").bindparams(
                        user_id=user_id, org_name=organization_name
                    )
                )
                session.commit()
        yield AuthState.login(form_data)

    @rx.event
    def login(self, form_data: dict):
        self.error_message = ""
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            self.error_message = "Email and password are required."
            return
        with rx.session() as session:
            user_row = session.exec(
                text(
                    "SELECT id, email, password_hash, role, full_name FROM user WHERE email = :email"
                ).bindparams(email=email)
            ).first()
            if user_row and self._verify_password(password, user_row.password_hash):
                self.is_authenticated = True
                self.current_user_email = user_row.email
                self.current_user_role = user_row.role
                self.current_user_name = user_row.full_name
                self.current_user_id = user_row.id
                self.error_message = ""
                return rx.redirect("/")
            else:
                self.error_message = "Invalid email or password."

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.current_user_email = ""
        self.current_user_role = ""
        self.current_user_name = ""
        self.current_user_id = None
        return rx.redirect("/")

    @rx.var
    def initial(self) -> str:
        return self.current_user_name[0].upper() if self.current_user_name else ""