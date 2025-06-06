from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models.product import Product
from app.utils.decorators import admin_required
from flask_login import login_required
# Import forms if using Flask-WTF later

bp = Blueprint("products", __name__, url_prefix="/products")

@bp.route("/")
@login_required
@admin_required
def list_products():
    page = request.args.get("page", 1, type=int)
    per_page = 10 # Or get from config
    products = Product.query.order_by(Product.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("products/list.html", products=products, title="Gerenciar Produtos")

@bp.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price_str = request.form.get("price")

        if not name or not price_str:
            flash("Nome e Preço são obrigatórios.", "danger")
            return render_template("products/form.html", title="Adicionar Produto")

        try:
            price = float(price_str.replace(",", ".")) # Handle comma as decimal separator
        except ValueError:
            flash("Preço inválido.", "danger")
            return render_template("products/form.html", title="Adicionar Produto")

        new_product = Product(name=name, description=description, price=price)
        db.session.add(new_product)
        try:
            db.session.commit()
            flash("Produto adicionado com sucesso!", "success")
            return redirect(url_for("products.list_products"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao adicionar produto: {e}", "danger")

    return render_template("products/form.html", title="Adicionar Produto", product=None) # Pass product=None for add form

@bp.route("/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price_str = request.form.get("price")

        if not name or not price_str:
            flash("Nome e Preço são obrigatórios.", "danger")
            return render_template("products/form.html", title="Editar Produto", product=product)

        try:
            price = float(price_str.replace(",", "."))
        except ValueError:
            flash("Preço inválido.", "danger")
            return render_template("products/form.html", title="Editar Produto", product=product)

        product.name = name
        product.description = description
        product.price = price
        try:
            db.session.commit()
            flash("Produto atualizado com sucesso!", "success")
            return redirect(url_for("products.list_products"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar produto: {e}", "danger")

    return render_template("products/form.html", title="Editar Produto", product=product)

@bp.route("/delete/<int:product_id>", methods=["POST"])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash("Produto excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir produto: {e}. Verifique se não está associado a pedidos.", "danger")
    return redirect(url_for("products.list_products"))


