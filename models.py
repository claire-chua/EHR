from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True,nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
