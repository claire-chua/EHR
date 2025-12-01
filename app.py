from flask import Flask, render_template, request, redirect, url_for, session, current_app, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TextAreaField
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed
from sqlalchemy import select
from db import db
from models import User, EHR
import os
from dotenv import load_dotenv

# Create a flask app 
app = Flask(__name__)

load_dotenv()

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///EHR.db"
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")

#Initialise app with db extension

with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()

login_manager = LoginManager(app)

login_manager.login_view = 'login'
principals = Principal(app)



@login_manager.user_loader
def load_user(userid):
    user_id_int = int(userid)
    return db.session.get(User, user_id_int)

class LoginForm(FlaskForm):
    email = StringField()
    password = PasswordField()

# provider_need = RoleNeed('provider')
# provider_permission = RoleNeed('patient')
                         
# provider_permission = Permission(RoleNeed('provider'))
# patient_permission = Permission(RoleNeed('patient'))

# email = "healthcare.provider@gmail.com"
# password = "password"
class EditPatientForm(FlaskForm):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = StringField()
    address = StringField()
    phone_no = StringField()
    emergency_phone_no = StringField()
    medical_history = TextAreaField()


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None
    
    # if request.method =="POST":
    if request.method =="POST":
        # Retrieve email and password details from login form
        submittedEmail = form.email.data
        submittedPassword = form.password.data
        
        user = db.session.scalar(select(User).filter_by(email=submittedEmail))

        print(submittedEmail)
        print(submittedPassword)
        print(user)

        if user:
            print(user.role)
            print(user.password)
        # Check if credentials match
        if  user and submittedPassword == user.password and user.role == "provider":
            flash("Login successful")
            login_user(user)
            # Identity =(user.id)
            # identity.provides.add(RoleNeed(user.role))
            # identity_changed.send(current_app._get_current_object(),
            #                       identity=Identity(user.id))
            return redirect(url_for("providerdashboard"))
        elif user and submittedPassword == user.password and user.role == "patient":
            login_user(user)
            # identity_changed.send(current_app._get_current_object(),
            #                       identity=Identity(user.id))
            return redirect(url_for("patientdashboard"))
        else:
            flash("No account associated with email & password")
            return render_template("index.html")
    return render_template("index.html", error=error) 

@app.route("/providerdashboard")
@login_required
# @provider_permission.require()
def providerdashboard():
    patients = db.session.scalars(
        select(User).where(User.role == "patient")
    ).all()
    print(patients)
    return render_template("providerdashboard.html", patients=patients )

@app.route("/providerdashboard/patient/<int:user_id>")
@login_required
def providerpatientdashboard(user_id):
    user = db.session.get(User, user_id)
    ehr = user.ehr

    return render_template("providerpatientdashboard.html", patient=user, ehr=ehr )

@app.route("/providerdashboard/patient/<int:user_id>/edit", methods=["GET","POST"])
@login_required
def providerpatienteditdashboard(user_id):
    form = EditPatientForm()
    user = db.session.get(User, user_id)
    ehr = user.ehr

    #encrypt saved details
    if request.method == "POST":
        ehr.first_name = form.first_name.data
        ehr.last_name = form.last_name.data
        ehr.date_of_birth = form.date_of_birth.data
        ehr.gender = form.gender.data
        ehr.address = form.address.data
        ehr.phone_no = form.phone_no.data
        ehr.emergency_phone_no = form.emergency_phone_no.data
        ehr.medical_history = form.medical_history.data

        db.session.commit()
        flash("Patient record updated")

    #decrypt the form
    return render_template(
        "providerpatienteditdashboard.html",
        patient=user,
        ehr=ehr
        )

@app.route("/patientdashboard")
@login_required
#@patient_permission.require()
def patientdashboard():
    ehr = current_user.ehr
    return render_template("patientdashboard.html", ehr=ehr)

# Run code as script only, and not as an import
if __name__ == "__main__":
    app.run(debug=True)