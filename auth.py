from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():

    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

user = User.query.filter_by(email=email).first()

                if user:
           
            if user.check_password(password):
                login_user(user)
              
                next_page = request.args.get("next")
                return redirect(next_page or url_for("main.dashboard"))
            else:
              
                flash("Email ou senha inválidos.", "danger")
        else:
                      flash("Email ou senha inválidos.", "danger")

    return render_template("auth/login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você foi desconectado.", "info")
    return redirect(url_for("auth.login"))

