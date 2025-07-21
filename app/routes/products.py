from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models.product import Product
from flask_login import login_required, current_user
from app.utils.decorators import admin_required

bp = Blueprint("products", __name__, url_prefix="/products")

@bp.route("/")
@login_required
@admin_required
def list_products():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    products = Product.query.order_by(Product.name).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("products/list.html", products=products, title="Produtos")

@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = float(request.form.get("price"))
        category = request.form.get("category")
        is_active = bool(request.form.get("is_active"))

        new_product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            is_active=is_active
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        flash("Produto criado com sucesso!", "success")
        return redirect(url_for("products.list_products"))

    return render_template("products/form.html", title="Novo Produto")

@bp.route("/view/<int:product_id>")
@login_required
@admin_required
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("products/view.html", product=product, title=f"Produto: {product.name}")

@bp.route("/import", methods=["GET", "POST"])
@login_required
@admin_required
def import_products():
    if request.method == "POST":
        # Handle file upload and import logic here
        flash("Funcionalidade de importação em desenvolvimento.", "info")
        return redirect(url_for("products.list_products"))
    
    return render_template("products/import.html", title="Importar Produtos")

