from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory, Response, abort
from app import db
from app.models.expense import Expense
from app.models.user import User
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import io
# Import PDF and XML libraries later when needed
# from fpdf import FPDF
# import xml.etree.ElementTree as ET

bp = Blueprint("expenses", __name__, url_prefix="/expenses")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def query_expenses(apply_filters=True):
    """Helper function to query expenses based on user role and filters."""
    query = Expense.query
    
    # Role-based filtering
    if not current_user.is_admin:
        query = query.filter(Expense.seller_id == current_user.id)
    
    if apply_filters:
        # Get filter parameters from request.args
        date_from_str = request.args.get("date_from")
        date_to_str = request.args.get("date_to")
        expense_type = request.args.get("expense_type")
        seller_id_str = request.args.get("seller_id") # For admin

        try:
            if date_from_str:
                date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
                query = query.filter(Expense.date >= date_from)
            if date_to_str:
                date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()
                query = query.filter(Expense.date <= date_to)
        except ValueError:
            flash("Formato de data inválido para filtro (YYYY-MM-DD).", "warning")
            # Decide how to handle: ignore filter, return error, etc.
            # For now, ignore invalid date filters
            pass 

        if expense_type:
            query = query.filter(Expense.expense_type == expense_type)
            
        if current_user.is_admin and seller_id_str:
            try:
                seller_id = int(seller_id_str)
                query = query.filter(Expense.seller_id == seller_id)
            except ValueError:
                flash("ID de vendedor inválido para filtro.", "warning")
                pass # Ignore invalid seller ID
                
    return query

@bp.route("/")
@login_required
def list_expenses():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    
    query = query_expenses(apply_filters=True) # Use helper to get filtered query
    expenses_pagination = query.order_by(Expense.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    # Fetch sellers if admin for filter dropdown
    sellers = []
    if current_user.is_admin:
        sellers = User.query.filter_by(is_admin=False).order_by(User.username).all()
        
    expense_types = ["combustível", "pedagio", "Refeições", "Hotel", "Diversos"] # Or get from config/db

    return render_template("expenses/list.html", 
                           expenses=expenses_pagination, 
                           title="Minhas Despesas" if not current_user.is_admin else "Relatório de Despesas",
                           sellers=sellers, 
                           expense_types=expense_types,
                           filter_args=request.args # Pass current filters back to template for form and report links
                           )

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    if request.method == "POST":
        date_str = request.form.get("date")
        expense_type = request.form.get("expense_type")
        amount_str = request.form.get("amount")
        city = request.form.get("city")
        state = request.form.get("state")
        km_initial_str = request.form.get("km_initial")
        km_final_str = request.form.get("km_final")
        description = request.form.get("description")
        receipt_file = request.files.get("receipt")

        if not all([date_str, expense_type, amount_str, city, state]):
            flash("Data, Tipo, Valor, Cidade e Estado são obrigatórios.", "danger")
            expense_types = ["combustível", "pedagio", "Refeições", "Hotel", "Diversos"]
            return render_template("expenses/form.html", title="Registrar Despesa", expense_types=expense_types)

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            amount = float(amount_str.replace(",", "."))
            km_initial = float(km_initial_str.replace(",", ".")) if km_initial_str else None
            km_final = float(km_final_str.replace(",", ".")) if km_final_str else None
        except ValueError:
            flash("Formato inválido para Data, Valor ou KM.", "danger")
            expense_types = ["combustível", "pedagio", "Refeições", "Hotel", "Diversos"]
            return render_template("expenses/form.html", title="Registrar Despesa", expense_types=expense_types)

        filename = None
        if receipt_file and allowed_file(receipt_file.filename):
            filename = secure_filename(f"{current_user.id}_{int(datetime.now().timestamp())}_{receipt_file.filename}")
            upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            try:
                receipt_file.save(upload_path)
            except Exception as e:
                flash(f"Erro ao salvar anexo: {e}", "danger")
                expense_types = ["combustível", "pedagio", "Refeições", "Hotel", "Diversos"]
                return render_template("expenses/form.html", title="Registrar Despesa", expense_types=expense_types)
        elif receipt_file:
             flash("Tipo de arquivo de nota fiscal inválido.", "danger")
             expense_types = ["combustível", "pedagio", "Refeições", "Hotel", "Diversos"]
             return render_template("expenses/form.html", title="Registrar Despesa", expense_types=expense_types)

        new_expense = Expense(
            date=date,
            expense_type=expense_type,
            amount=amount,
            city=city,
            state=state,
            km_initial=km_initial,
            km_final=km_final,
            description=description,
            receipt_filename=filename,
            seller_id=current_user.id
        )
        new_expense.calculate_km_total()

        db.session.add(new_expense)
        try:
            db.session.commit()
            flash("Despesa registrada com sucesso!", "success")
            return redirect(url_for("expenses.list_expenses"))
        except Exception as e:
            db.session.rollback()
            if filename and os.path.exists(os.path.join(current_app.config["UPLOAD_FOLDER"], filename)):
                 try:
                     os.remove(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
                 except OSError:
                     pass 
            flash(f"Erro ao registrar despesa: {e}", "danger")

    expense_types = ["combustível", "pedagio", "Refeições", "Hotel", "Diversos"]
    return render_template("expenses/form.html", title="Registrar Despesa", expense_types=expense_types)

@bp.route("/view/<int:expense_id>")
@login_required
def view_expense(expense_id):
    query = Expense.query
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)
    expense = query.get_or_404(expense_id)
    return render_template("expenses/view.html", expense=expense, title=f"Despesa #{expense.id}")

@bp.route("/uploads/<filename>")
@login_required
def uploaded_file(filename):
    expense_record = Expense.query.filter_by(receipt_filename=filename).first()
    if not expense_record:
        return abort(404)
    if not current_user.is_admin and expense_record.seller_id != current_user.id:
        return abort(403)
        
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@bp.route("/report/txt")
@login_required
def generate_txt_report():
    # Use the same filters as the list view
    query = query_expenses(apply_filters=True)
    expenses = query.order_by(Expense.date.asc()).all()

    if not expenses:
        flash("Nenhuma despesa encontrada para gerar o relatório com os filtros aplicados.", "warning")
        return redirect(url_for("expenses.list_expenses", **request.args))

    output = io.StringIO()
    output.write("====================================================================================================\n")
    output.write(f"                     RELATÓRIO DE DESPESAS - New Agro Business \n")
    # Add filter info to header
    applied_filters = {k: v for k, v in request.args.items() if k != 'page'}
    output.write(f"Filtros Aplicados: {applied_filters}\n")
    output.write("====================================================================================================\n")
    output.write("{:<5} {:<12} {:<15} {:<15} {:<12} {:<15} {:<10} {:<10} {:<10} {:<15}\n".format(
        "ID", "Data", "Vendedor", "Tipo", "Valor (R$)", "Cidade/UF", "KM Ini", "KM Fim", "KM Total", "Anexo"
    ))
    output.write("----------------------------------------------------------------------------------------------------\n")

    total_geral = 0.0
    total_km = 0.0

    for expense in expenses:
        total_geral += expense.amount
        if expense.km_total is not None:
            total_km += expense.km_total
            
        output.write("{:<5} {:<12} {:<15} {:<15} {:<12.2f} {:<15} {:<10} {:<10} {:<10} {:<15}\n".format(
            expense.id,
            expense.date.strftime("%d/%m/%Y"),
            expense.seller.username[:14],
            expense.expense_type.capitalize()[:14],
            expense.amount,
            f"{expense.city}/{expense.state}"[:14],
            f"{expense.km_initial:.1f}" if expense.km_initial is not None else "-",
            f"{expense.km_final:.1f}" if expense.km_final is not None else "-",
            f"{expense.km_total:.1f}" if expense.km_total is not None else "-",
            expense.receipt_filename[:14] if expense.receipt_filename else "-"
        ))

    output.write("----------------------------------------------------------------------------------------------------\n")
    output.write(f"TOTAL GERAL DESPESAS: R$ {total_geral:.2f}\n")
    output.write(f"TOTAL KM RODADO: {total_km:.1f} KM\n")
    output.write("====================================================================================================\n")

    report_content = output.getvalue()
    output.close()

    # Generate filename based on filters/date
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"relatorio_despesas_{timestamp}.txt"

    return Response(
        report_content,
        mimetype="text/plain",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )

# TODO: Add routes for PDF and XML reports
# @bp.route("/report/pdf")
# @login_required
# def generate_pdf_report():
#     pass

# @bp.route("/report/xml")
# @login_required
# def generate_xml_report():
#     pass

# Add routes for editing/deleting expenses later if needed

