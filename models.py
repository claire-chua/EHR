from sqlalchemy import Integer, String, ForeignKey, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import db
from flask_login import UserMixin
from datetime import date
from crypto_utils import encrypt_text, decrypt_text

#user table model
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True,nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

    ehr: Mapped["EHR"] = relationship(
        back_populates="user",
        uselist=False
    )

#EHR model
class EHR(db.Model):
    id: Mapped[int] = mapped_column (primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
        unique=True,
    )
    _first_name: Mapped[str] = mapped_column("first_name", String(20), nullable=False)
    _last_name: Mapped[str] = mapped_column("last_name", String(50), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    _gender: Mapped[str] = mapped_column("gender", String(10), nullable=False)
    _address: Mapped[str] = mapped_column( "address", String(255), nullable=False)
    _phone_no: Mapped[str] = mapped_column("phone_no", String(30), nullable=False)
    _emergency_phone_no: Mapped[str] = mapped_column("emergency_phone_no", String(30), nullable=False)

    _medical_history: Mapped[str] = mapped_column("medical_history", Text, nullable =False)

    user: Mapped["User"] = relationship(back_populates="ehr")

    @property
    def first_name(self) -> str:
        return decrypt_text(self._first_name)
    
    @first_name.setter
    def first_name(self, value: str):
        self._first_name = encrypt_text(value)

    @property
    def last_name(self) -> str:
        return decrypt_text(self._last_name)
    
    @last_name.setter
    def last_name(self, value: str):
        self._last_name = encrypt_text(value)
    
    @property
    def gender(self) -> str:
        return decrypt_text(self._gender)
    
    @gender.setter
    def gender(self, value: str):
        self._gender = encrypt_text(value)

    @property
    def address(self) -> str:
        return decrypt_text(self._address)
    
    @address.setter
    def address(self, value: str):
        self._address = encrypt_text(value)

    @property
    def phone_no(self) -> str:
        return decrypt_text(self._phone_no)
    
    @phone_no.setter
    def phone_no(self, value: str):
        self._phone_no = encrypt_text(value)

    @property
    def emergency_phone_no(self) -> str:
        return decrypt_text(self._emergency_phone_no)
    
    @emergency_phone_no.setter
    def emergency_phone_no(self, value: str):
        self._emergency_phone_no = encrypt_text(value)

    @property
    def medical_history(self) -> str:
        return decrypt_text(self._medical_history)
    
    @medical_history.setter
    def medical_history(self, value: str):
        self._medical_history = encrypt_text(value)
