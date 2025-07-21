from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from app import db
from app.models.expense import Expense
from flask_login import login_required, current_user
from datetime import datetime
import io

bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@bp.route("/")
@login_required
def list_expenses():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    query = Expense.query
    # Admins see all expenses, sellers only see their own
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)

    expenses = query.order_by(Expense.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("expenses/list.html", expenses=expenses, title="Minhas Despesas" if not current_user.is_admin else "Todas as Despesas")

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_expense():
    if request.method == "POST":
        date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
        expense_type = request.form.get("expense_type")
        amount = float(request.form.get("amount"))
        description = request.form.get("description")
        city = request.form.get("city")
        state = request.form.get("state")
        km_initial = request.form.get("km_initial")
        km_final = request.form.get("km_final")

        # Convert km values to float if provided
        km_initial = float(km_initial) if km_initial else None
        km_final = float(km_final) if km_final else None

        new_expense = Expense(
            date=date,
            expense_type=expense_type,
            amount=amount,
            description=description,
            city=city,
            state=state,
            km_initial=km_initial,
            km_final=km_final,
            seller_id=current_user.id
        )
        
        new_expense.calculate_km_total()
        
        db.session.add(new_expense)
        db.session.commit()
        
        flash("Despesa registrada com sucesso!", "success")
        return redirect(url_for("expenses.list_expenses"))

    return render_template("expenses/form.html", title="Nova Despesa")

@bp.route("/view/<int:expense_id>")
@login_required
def view_expense(expense_id):
    query = Expense.query
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)
    expense = query.get_or_404(expense_id)
    return render_template("expenses/view.html", expense=expense, title=f"Despesa #{expense.id}")

@bp.route("/report/txt")
@login_required
def generate_txt_report():
    query = Expense.query
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)
    
    expenses = query.order_by(Expense.date.desc()).all()

    output = io.StringIO()
    output.write("========================================\n")
    output.write("    RELATÓRIO DE DESPESAS - New Agro Business\n")
    output.write("========================================\n")
    output.write(f"Vendedor: {current_user.username}\n")
    output.write(f"Data do Relatório: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    output.write("----------------------------------------\n")

    total_amount = 0
    for expense in expenses:
        output.write(f"Data: {expense.date.strftime('%d/%m/%Y')}\n")
        output.write(f"Tipo: {expense.expense_type}\n")
        output.write(f"Valor: R$ {expense.amount:.2f}\n")
        output.write(f"Local: {expense.city}/{expense.state}\n")
        if expense.description:
            output.write(f"Descrição: {expense.description}\n")
        if expense.km_total:
            output.write(f"KM Total: {expense.km_total:.2f}\n")
        output.write("----------------------------------------\n")
        total_amount += expense.amount

    output.write(f"TOTAL GERAL: R$ {total_amount:.2f}\n")
    output.write("========================================\n")

    report_content = output.getvalue()
    output.close()

    return Response(
        report_content,
        mimetype="text/plain",
        headers={"Content-disposition": f"attachment; filename=despesas_{current_user.username}.txt"}
    )

