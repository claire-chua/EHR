from app import app, db
from models import User, EHR
from datetime import date

def add_user(email, password, role, ehr_data=None):
    user = User(
        email=email,
        role=role,
        password=password
        )
    db.session.add(user)
    
    if role == "patient":
        ehr = EHR(
            user=user,
            first_name= ehr_data["first_name"],
            last_name=ehr_data["last_name"],
            date_of_birth=ehr_data["date_of_birth"],
            gender=ehr_data["gender"],
            address=ehr_data["address"],
            phone_no=ehr_data["phone_no"],
            emergency_phone_no=ehr_data["emergency_phone_no"],
            medical_history=ehr_data["medical_history"],
        )
        db.session.add(ehr)
    
    db.session.commit()
    return user

with app.app_context():
    db.drop_all()
    db.create_all()
    
    provider = add_user(
        email="florence.nightingale@gmail.com",
        password="nurse",
        role="provider",
        ehr_data=None
    )
    print(f"Added Provider: {provider.email}")

    patient = add_user(
        email="marie.sklodowska@gmail.com",
        password="nobels",
        role="patient",
        ehr_data={
            "first_name": "Marie",
            "last_name": "Sklodowska",
            "date_of_birth": date(2000, 11, 7),
            "gender": "Female",
            "address": "11 Smith St",
            "phone_no": "000000000",
            "emergency_phone_no": "000000001",
            "medical_history": "Depression",
        }
    )
    print(f"Added Patient: {patient.email}")

    patient = add_user(
        email="katherine.johnson@gmail.com",
        password="nasa",
        role="patient",
        ehr_data={
            "first_name": "Katherine",
            "last_name": "Johnson",
            "date_of_birth": date(2000, 8, 26),
            "gender": "Female",
            "address": "1 Elizabeth St",
            "phone_no": "000000000",
            "emergency_phone_no": "000000001",
            "medical_history": "N/A",
        }
    )
    print(f"Added Patient: {patient.email}")



