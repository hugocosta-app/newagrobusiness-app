from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from app.models.user import User
# You might need a form class later, e.g., using Flask-WTF
# from app.forms import LoginForm

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard")) # Redirect if already logged in

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Email ou senha inválidos.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember)
        flash("Login realizado com sucesso!", "success")

        # Redirect to the page the user was trying to access, or dashboard
        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.dashboard"))

    # For GET request, just render the login page
    return render_template("auth/login.html", title="Login")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso.", "info")
    return redirect(url_for("auth.login"))

# Optional: Add a route for initial admin setup or user registration if needed
# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     # Implementation for user registration
#     pass

