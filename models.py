from sqlalchemy import Integer, String, ForeignKey, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import db
from flask_login import UserMixin

from datetime import datetime, date

#user table model
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True,nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

    EHR: Mapped["EHR"] = relationship(
        back_populated="user",
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
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_no: Mapped[str] = mapped_column(String(30), nullable=False)
    emergency_phone_no: Mapped[str] = mapped_column(String(30), nullable =True)

    medical_history: Mapped[str] = mapped_column(Text, nullable =True)

    user: Mapped["User"] = relationship(back_populates="EHR")
