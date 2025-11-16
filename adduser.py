from app import app, db
from models import User

def add_user(email, password, role):
    user = User(email=email, role=role,password=password)

    db.session.add(user)

    db.session.commit()

    return user


with app.app_context():
    provider = add_user(
        email="provider@gmail.com",
        password="password",
        role="provider",
    )
    print(f"Added Provider: {provider.email}")

    patient = add_user(
        email="patient@gmail.com",
        password="password",
        role="patient",
    )
    print(f"Added Patient: {patient.email}")