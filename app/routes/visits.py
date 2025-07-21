from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models.visit import Visit
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint("visits", __name__, url_prefix="/visits")

@bp.route("/")
@login_required
def list_visits():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    query = Visit.query
    # Admins see all visits, sellers only see their own
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)

    visits = query.order_by(Visit.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("visits/list.html", visits=visits, title="Minhas Visitas" if not current_user.is_admin else "Todas as Visitas")

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_visit():
    if request.method == "POST":
        date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
        customer_name = request.form.get("customer_name")
        customer_cnpj = request.form.get("customer_cnpj")
        city = request.form.get("city")
        state = request.form.get("state")
        summary = request.form.get("summary")
        highlights = request.form.get("highlights")
        observations = request.form.get("observations")

        new_visit = Visit(
            date=date,
            customer_name=customer_name,
            customer_cnpj=customer_cnpj,
            city=city,
            state=state,
            summary=summary,
            highlights=highlights,
            observations=observations,
            seller_id=current_user.id
        )
        
        db.session.add(new_visit)
        db.session.commit()
        
        flash("Visita registrada com sucesso!", "success")
        return redirect(url_for("visits.list_visits"))

    return render_template("visits/form.html", title="Nova Visita")

@bp.route("/view/<int:visit_id>")
@login_required
def view_visit(visit_id):
    query = Visit.query
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)
    visit = query.get_or_404(visit_id)
    return render_template("visits/view.html", visit=visit, title=f"Visita #{visit.id}")

