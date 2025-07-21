from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
from app.utils.decorators import admin_required

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
                
                # Redirect based on user role if no next page specified
                if not next_page:
                    if user.is_admin:
                        next_page = url_for("main.dashboard")
                    else:
                        next_page = url_for("main.seller_dashboard")
                
                return redirect(next_page)
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

@bp.route("/register", methods=["GET", "POST"])
@login_required
@admin_required
def register():
    """Permite que administradores registrem novos vendedores"""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        nickname = request.form.get("nickname")
        
        # Verificar se o usuário já existe
        if User.query.filter_by(email=email).first():
            flash("Email já está em uso.", "danger")
            return render_template("auth/register.html")
        
        if User.query.filter_by(username=username).first():
            flash("Nome de usuário já está em uso.", "danger")
            return render_template("auth/register.html")
        
        # Criar novo vendedor
        try:
            User.create_user(username, email, password, is_admin=False, nickname=nickname)
            flash(f"Vendedor {username} criado com sucesso!", "success")
            return redirect(url_for("auth.list_users"))
        except Exception as e:
            flash(f"Erro ao criar vendedor: {e}", "danger")
    
    return render_template("auth/register.html", title="Registrar Vendedor")

@bp.route("/users")
@login_required
@admin_required
def list_users():
    """Lista todos os usuários para administradores"""
    users = User.query.order_by(User.username).all()
    return render_template("auth/users.html", users=users, title="Gerenciar Usuários")

