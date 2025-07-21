from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models.agenda import AgendaEntry
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint("agenda", __name__, url_prefix="/agenda")

@bp.route("/")
@login_required
def view_agenda():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    query = AgendaEntry.query
    # Admins see all agenda entries, sellers only see their own
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)

    agenda_entries = query.order_by(AgendaEntry.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    title = "Minha Agenda" if not current_user.is_admin else "Agenda da Equipe"
    return render_template("agenda/list.html", agenda_entries=agenda_entries, title=title)

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_entry():
    if request.method == "POST":
        date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
        time_str = request.form.get("time")
        time = datetime.strptime(time_str, "%H:%M").time() if time_str else None
        location = request.form.get("location")
        description = request.form.get("description")
        status = request.form.get("status", "Agendado")

        new_entry = AgendaEntry(
            date=date,
            time=time,
            location=location,
            description=description,
            status=status,
            seller_id=current_user.id
        )
        
        db.session.add(new_entry)
        db.session.commit()
        
        flash("Compromisso agendado com sucesso!", "success")
        return redirect(url_for("agenda.view_agenda"))

    return render_template("agenda/form.html", title="Novo Compromisso")

@bp.route("/view/<int:entry_id>")
@login_required
def view_entry(entry_id):
    query = AgendaEntry.query
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)
    entry = query.get_or_404(entry_id)
    return render_template("agenda/view.html", entry=entry, title=f"Compromisso #{entry.id}")

