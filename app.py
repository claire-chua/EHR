from contextlib import redirect_stderr
from flask import Flask, render_template, request

# Create a flask app
app = Flask(__name__)

email = "healthcare.provider@gmail.com"
password = "password"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method =="POST":
        # Retrieve email and password details from login form
        getEmail = request.form.get("email")
        getPassword = request.form.get("password")

        # Check if credentials match
        if  getEmail == email and getPassword == password:
            return render_template("healthcareproviderdashboard.html")
        else:
            return render_template("index.html", error="There is no account associated with this email and password.")
    return render_template("index.html")

# Run code as script only, and not as an import
if __name__ == "__main__":
    app.run(debug=True)