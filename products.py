from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models.product import Product
from app.utils.decorators import admin_required
from flask_login import login_required
import openpyxl
import os

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
        stock_str = request.form.get("stock")

        if not name or not price_str or not stock_str:
            flash("Nome, Preço e Estoque são obrigatórios.", "danger")
            return render_template("products/form.html", title="Adicionar Produto")

        try:
            price = float(price_str.replace(",", ".")) # Handle comma as decimal separator
            stock = int(stock_str)
        except ValueError:
            flash("Preço ou Estoque inválido.", "danger")
            return render_template("products/form.html", title="Adicionar Produto")

        new_product = Product(name=name, description=description, price=price, stock=stock)
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
        stock_str = request.form.get("stock")

        if not name or not price_str or not stock_str:
            flash("Nome, Preço e Estoque são obrigatórios.", "danger")
            return render_template("products/form.html", title="Editar Produto", product=product)

        try:
            price = float(price_str.replace(",", "."))
            stock = int(stock_str)
        except ValueError:
            flash("Preço ou Estoque inválido.", "danger")
            return render_template("products/form.html", title="Editar Produto", product=product)

        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
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

@bp.route("/import", methods=["GET", "POST"])
@login_required
@admin_required
def import_products():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Nenhum arquivo selecionado.", "danger")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("Nenhum arquivo selecionado.", "danger")
            return redirect(request.url)
        if file and file.filename.endswith((".xlsx", ".xls")):
            try:
                # Save the file temporarily
                filepath = os.path.join("/tmp", file.filename)
                file.save(filepath)

                workbook = openpyxl.load_workbook(filepath)
                sheet = workbook.active
                imported_count = 0
                errors = []

                # Assuming first row is header: Nome, Preço, Estoque, Descrição (optional)
                for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
                    try:
                        name = row[0]
                        price = float(str(row[1]).replace(",", "."))
                        stock = int(row[2])
                        description = row[3] if len(row) > 3 else None

                        if not name or price is None or stock is None:
                            errors.append(f"Linha {row_index+1}: Dados incompletos (Nome, Preço ou Estoque).")
                            continue

                        # Check if product already exists by name
                        existing_product = Product.query.filter_by(name=name).first()
                        if existing_product:
                            existing_product.price = price
                            existing_product.stock = stock
                            existing_product.description = description
                            db.session.add(existing_product)
                            flash(f"Produto \'{name}\' atualizado.", "info")
                        else:
                            new_product = Product(name=name, price=price, stock=stock, description=description)
                            db.session.add(new_product)
                            flash(f"Produto \'{name}\' adicionado.", "success")
                        imported_count += 1
                    except Exception as e:
                        errors.append(f"Linha {row_index+1}: Erro ao processar - {e}")
                        db.session.rollback() # Rollback current transaction if error occurs

                db.session.commit() # Commit all successful changes at once
                flash(f"Importação concluída. {imported_count} produtos processados.", "success")
                if errors:
                    flash("Alguns erros ocorreram durante a importação:\n" + "\n".join(errors), "warning")

                os.remove(filepath) # Clean up temporary file
                return redirect(url_for("products.list_products"))

            except Exception as e:
                flash(f"Erro ao importar arquivo: {e}", "danger")
                return redirect(request.url)
        else:
            flash("Formato de arquivo inválido. Por favor, use .xlsx ou .xls.", "danger")
            return redirect(request.url)

    return render_template("products/import.html", title="Importar Produtos")


