from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app import db
from app.models.agenda import AgendaEntry
from app.models.user import User # For admin view
from flask_login import login_required, current_user
from datetime import date, timedelta, datetime

bp = Blueprint("agenda", __name__, url_prefix="/agenda")

def get_week_dates(target_date=None):
    """Returns the start (Monday) and end (Sunday) dates of the week containing target_date."""
    if target_date is None:
        target_date = date.today()
    start_of_week = target_date - timedelta(days=target_date.weekday()) # Monday
    end_of_week = start_of_week + timedelta(days=6) # Sunday
    return start_of_week, end_of_week

@bp.route("/") # Seller's weekly view / Admin's overview
@login_required
def view_agenda():
    target_date_str = request.args.get("date")
    target_date = None
    if target_date_str:
        try:
            target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Data inválida para visualização da agenda.", "warning")
            target_date = date.today()
    else:
        target_date = date.today()

    start_week, end_week = get_week_dates(target_date)
    
    if current_user.is_admin:
        # Admin view: Show all entries for the selected week, grouped by seller?
        # Or maybe a daily view for all sellers?
        # Let's start with a list view for the selected date for all sellers.
        selected_date_str = request.args.get("selected_date", start_week.strftime("%Y-%m-%d"))
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = start_week
            
        entries = AgendaEntry.query.filter(
            AgendaEntry.entry_date == selected_date
        ).order_by(AgendaEntry.seller_id, AgendaEntry.created_at).all()
        
        sellers = User.query.filter_by(is_admin=False).order_by(User.username).all()
        
        return render_template("agenda/admin_view.html", 
                               title="Agenda da Equipe", 
                               entries=entries, 
                               sellers=sellers,
                               selected_date=selected_date)
    else:
        # Seller view: Show their entries for the current/selected week
        entries = AgendaEntry.query.filter(
            AgendaEntry.seller_id == current_user.id,
            AgendaEntry.entry_date >= start_week,
            AgendaEntry.entry_date <= end_week
        ).order_by(AgendaEntry.entry_date).all()
        
        # Organize entries by date for the template
        entries_by_date = { (start_week + timedelta(days=i)): [] for i in range(7) }
        for entry in entries:
            if entry.entry_date in entries_by_date:
                entries_by_date[entry.entry_date].append(entry)
                
        # Calculate previous and next week dates for navigation
        prev_week_date = start_week - timedelta(days=7)
        next_week_date = start_week + timedelta(days=7)

        return render_template("agenda/seller_view.html", 
                               title="Minha Agenda Semanal", 
                               entries_by_date=entries_by_date, 
                               start_week=start_week, 
                               end_week=end_week,
                               prev_week_date=prev_week_date,
                               next_week_date=next_week_date)

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_entry():
    if current_user.is_admin:
        flash("Administradores não registram agenda.", "warning")
        return redirect(url_for("agenda.view_agenda"))
        
    if request.method == "POST":
        entry_date_str = request.form.get("entry_date")
        location = request.form.get("location")
        description = request.form.get("description")

        if not all([entry_date_str, location]):
            flash("Data e Localização são obrigatórios.", "danger")
            return render_template("agenda/form.html", title="Adicionar Compromisso")

        try:
            entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Formato de Data inválido.", "danger")
            return render_template("agenda/form.html", title="Adicionar Compromisso")

        new_entry = AgendaEntry(
            entry_date=entry_date,
            location=location,
            description=description,
            seller_id=current_user.id
        )
        db.session.add(new_entry)
        try:
            db.session.commit()
            flash("Compromisso adicionado com sucesso!", "success")
            # Redirect to the week view containing the new entry date
            return redirect(url_for("agenda.view_agenda", date=entry_date.strftime("%Y-%m-%d")))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao adicionar compromisso: {e}", "danger")

    # GET request - pre-fill date if provided
    prefill_date_str = request.args.get("date", date.today().strftime("%Y-%m-%d"))
    return render_template("agenda/form.html", title="Adicionar Compromisso", prefill_date=prefill_date_str)

@bp.route("/edit/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = AgendaEntry.query.get_or_404(entry_id)
    # Ensure seller can only edit their own entries
    if entry.seller_id != current_user.id and not current_user.is_admin:
        abort(403)
    # Admins shouldn't edit directly, maybe view only?
    if current_user.is_admin:
         flash("Administradores não podem editar diretamente a agenda dos vendedores.", "warning")
         return redirect(url_for("agenda.view_agenda"))

    if request.method == "POST":
        entry_date_str = request.form.get("entry_date")
        location = request.form.get("location")
        description = request.form.get("description")

        if not all([entry_date_str, location]):
            flash("Data e Localização são obrigatórios.", "danger")
            return render_template("agenda/form.html", title="Editar Compromisso", entry=entry)

        try:
            entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Formato de Data inválido.", "danger")
            return render_template("agenda/form.html", title="Editar Compromisso", entry=entry)

        entry.entry_date = entry_date
        entry.location = location
        entry.description = description
        entry.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            flash("Compromisso atualizado com sucesso!", "success")
            return redirect(url_for("agenda.view_agenda", date=entry.entry_date.strftime("%Y-%m-%d")))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar compromisso: {e}", "danger")

    # GET request
    return render_template("agenda/form.html", title="Editar Compromisso", entry=entry)

@bp.route("/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = AgendaEntry.query.get_or_404(entry_id)
    if entry.seller_id != current_user.id and not current_user.is_admin:
        abort(403)
    if current_user.is_admin:
         flash("Administradores não podem excluir diretamente a agenda dos vendedores.", "warning")
         return redirect(url_for("agenda.view_agenda"))

    target_date_redirect = entry.entry_date.strftime("%Y-%m-%d")
    try:
        db.session.delete(entry)
        db.session.commit()
        flash("Compromisso excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir compromisso: {e}", "danger")
        
    return redirect(url_for("agenda.view_agenda", date=target_date_redirect))


