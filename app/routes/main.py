from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.order import Order
from app.models.expense import Expense
from app.models.visit import Visit
from app.models.agenda import AgendaEntry
from app import db

bp = Blueprint("main", __name__)

@bp.route("/")
@bp.route("/dashboard")
@login_required
def dashboard():
    # Redirect based on user role
    if current_user.is_admin:
        return admin_dashboard()
    else:
        return seller_dashboard()

def admin_dashboard():
    """Dashboard para administradores com visão geral de todos os dados"""
    # Estatísticas gerais
    total_orders = Order.query.count()
    total_expenses = Expense.query.count()
    total_visits = Visit.query.count()
    
    # Pedidos recentes
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    
    # Despesas recentes
    recent_expenses = Expense.query.order_by(Expense.date.desc()).limit(5).all()
    
    return render_template("dashboard.html", 
                         title="Dashboard - Admin",
                         total_orders=total_orders,
                         total_expenses=total_expenses,
                         total_visits=total_visits,
                         recent_orders=recent_orders,
                         recent_expenses=recent_expenses)

@bp.route("/seller-dashboard")
@login_required
def seller_dashboard():
    """Dashboard específico para vendedores com apenas seus dados"""
    if current_user.is_admin:
        return redirect(url_for("main.dashboard"))
    
    # Estatísticas do vendedor
    my_orders = Order.query.filter_by(seller_id=current_user.id).count()
    my_expenses = Expense.query.filter_by(seller_id=current_user.id).count()
    my_visits = Visit.query.filter_by(seller_id=current_user.id).count()
    
    # Dados recentes do vendedor
    recent_orders = Order.query.filter_by(seller_id=current_user.id).order_by(Order.order_date.desc()).limit(5).all()
    recent_expenses = Expense.query.filter_by(seller_id=current_user.id).order_by(Expense.date.desc()).limit(5).all()
    recent_visits = Visit.query.filter_by(seller_id=current_user.id).order_by(Visit.date.desc()).limit(3).all()
    
    # Próximos compromissos
    upcoming_agenda = AgendaEntry.query.filter_by(seller_id=current_user.id).order_by(AgendaEntry.date.asc()).limit(3).all()
    
    return render_template("seller_view.html", 
                         title="Meu Dashboard",
                         my_orders=my_orders,
                         my_expenses=my_expenses,
                         my_visits=my_visits,
                         recent_orders=recent_orders,
                         recent_expenses=recent_expenses,
                         recent_visits=recent_visits,
                         upcoming_agenda=upcoming_agenda)

