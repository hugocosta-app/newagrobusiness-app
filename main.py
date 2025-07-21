from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint("main", __name__)

@bp.route("/")
@bp.route("/dashboard")
@login_required
def dashboard():
    # This will be the main dashboard after login
    # Content can be customized based on user role (admin/seller)
    return render_template("dashboard.html", title="Dashboard")

# Add other main routes here as needed, e.g., a public landing page if required
# @bp.route("/home")
# def home():
#     return render_template("home.html") # Example public page

