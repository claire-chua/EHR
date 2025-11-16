from flask import Flask, render_template, request, redirect, url_for, session, current_app, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed
from sqlalchemy import select
from db import db
from models import User

# Create a flask app 
app = Flask(__name__)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///EHR.db"
app.config['SECRET_KEY'] = 'secret'

#Initialise app with db extension

with app.app_context():
    db.init_app(app)
    db.create_all()

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
        # Check if credentials match
        if  user and submittedPassword == user.password and user.role == "provider":
            flash("Login successful")
            # login_user(user)
            # Identity =(user.id)
            # identity.provides.add(RoleNeed(user.role))
            # identity_changed.send(current_app._get_current_object(),
            #                       identity=Identity(user.id))
            return redirect(url_for("providerdashboard"))
        elif user and submittedPassword == user.password and user.role == "patient":
            # login_user(user)
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
    return render_template("providerdashboard.html")

@app.route("/patientdashboard")
@login_required
#@patient_permission.require()
def patientdashboard():
    return render_template("patientdashboard.html")

# Run code as script only, and not as an import
if __name__ == "__main__":
    app.run(debug=True)