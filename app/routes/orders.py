from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, Response
from app import db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from flask_login import login_required, current_user
from datetime import datetime
import io

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.route("/")
@login_required
def list_orders():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    query = Order.query
    # Admins see all orders, sellers only see their own
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)

    orders = query.order_by(Order.order_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("orders/list.html", orders=orders, title="Meus Pedidos" if not current_user.is_admin else "Todos os Pedidos")

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_order():
    if request.method == "POST":
        customer_name = request.form.get("customer_name")
        customer_cnpj = request.form.get("customer_cnpj")
        delivery_address = request.form.get("delivery_address")
        product_ids = request.form.getlist("product_id[]")
        quantities = request.form.getlist("quantity[]")
        discounts = request.form.getlist("discount[]")

        if not all([customer_name, customer_cnpj, delivery_address, product_ids, quantities]):
            flash("Todos os campos do cliente e pelo menos um produto são obrigatórios.", "danger")
            products = Product.query.order_by(Product.name).all()
            return render_template("orders/create.html", title="Novo Pedido", products=products)

        # Basic validation
        if len(product_ids) != len(quantities) or len(product_ids) != len(discounts):
             flash("Erro nos dados dos produtos do pedido.", "danger")
             products = Product.query.order_by(Product.name).all()
             return render_template("orders/create.html", title="Novo Pedido", products=products)

        new_order = Order(
            customer_name=customer_name,
            customer_cnpj=customer_cnpj,
            delivery_address=delivery_address,
            seller_id=current_user.id
        )
        db.session.add(new_order)

        total_order_value = 0
        order_items_to_add = []

        try:
            for i in range(len(product_ids)):
                product_id = int(product_ids[i])
                quantity = int(quantities[i])
                discount = float(discounts[i] or 0.0)

                if quantity <= 0:
                    raise ValueError(f"Quantidade inválida para o produto ID {product_id}.")
                if not (0 <= discount <= 100):
                     raise ValueError(f"Desconto inválido (0-100) para o produto ID {product_id}.")

                product = Product.query.get(product_id)
                if not product:
                    raise ValueError(f"Produto ID {product_id} não encontrado.")

                order_item = OrderItem(
                    order=new_order,
                    product_id=product.id,
                    quantity=quantity,
                    price_at_order=product.price,
                    discount_applied=discount
                )
                order_items_to_add.append(order_item)

            # Add all items to session AFTER loop
            db.session.add_all(order_items_to_add)

            # Calculate total after adding items
            new_order.calculate_total()

            db.session.commit()
            flash("Pedido criado com sucesso!", "success")
            return redirect(url_for("orders.view_order", order_id=new_order.id))

        except ValueError as ve:
            db.session.rollback()
            flash(f"Erro ao processar itens do pedido: {ve}", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar pedido: {e}", "danger")

        # If error occurred, reload form with products
        products = Product.query.order_by(Product.name).all()
        return render_template("orders/create.html", title="Novo Pedido", products=products)

    # GET request
    products = Product.query.order_by(Product.name).all()
    return render_template("orders/create.html", title="Novo Pedido", products=products)

@bp.route("/view/<int:order_id>")
@login_required
def view_order(order_id):
    query = Order.query
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)
    order = query.get_or_404(order_id)
    return render_template("orders/view.html", order=order, title=f"Pedido #{order.id}")

@bp.route("/search_products")
@login_required
def search_products():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])

    products = Product.query.filter(Product.name.ilike(f"%{query}%")).limit(10).all()
    results = [{
        "id": p.id,
        "name": p.name,
        "price": p.price
    } for p in products]
    return jsonify(results)

@bp.route("/report/txt/<int:order_id>")
@login_required
def generate_txt_report(order_id):
    query = Order.query
    if not current_user.is_admin:
        query = query.filter_by(seller_id=current_user.id)
    order = query.get_or_404(order_id)

    output = io.StringIO()
    output.write("========================================\n")
    output.write(f"         PEDIDO #{order.id} - New Agro Business \n")
    output.write("========================================\n")
    formatted_date = order.order_date.strftime('%d/%m/%Y %H:%M:%S')
    output.write(f"Data do Pedido: {formatted_date}\n")

    output.write(f"Vendedor: {order.seller.username}\n")
    output.write("----------------------------------------\n")
    output.write("Dados do Cliente:\n")
    output.write(f"  Nome: {order.customer_name}\n")
    output.write(f"  CNPJ: {order.customer_cnpj}\n")
    output.write("  Endereço de Entrega:\n")
    for line in order.delivery_address.split("\n"):
        output.write(f"    {line.strip()}\n")
    output.write("----------------------------------------\n")
    output.write("Itens do Pedido:\n")
    output.write("{:<5} {:<30} {:>10} {:>10} {:>10} {:>12}\n".format(
        "ID", "Produto", "Qtd", "Preço Unit", "Desc(%) ", "Subtotal"
    ))
    output.write("------------------------------------------------------------------------\n")

    for item in order.items:
        subtotal = item.quantity * item.price_at_order
        discount_amount = subtotal * (item.discount_applied / 100.0)
        final_subtotal = subtotal - discount_amount
        output.write("{:<5} {:<30} {:>10} {:>10.2f} {:>10.1f} {:>12.2f}\n".format(
            item.product_id,
            item.product.name[:30],
            item.quantity,
            item.price_at_order,
            item.discount_applied,
            final_subtotal
        ))

    output.write("------------------------------------------------------------------------\n")
    output.write(f"Valor Total do Pedido: R$ {order.total_amount:.2f}\n")
    output.write("========================================\n")

    report_content = output.getvalue()
    output.close()

    return Response(
        report_content,
        mimetype="text/plain",
        headers={"Content-disposition": f"attachment; filename=pedido_{order.id}.txt"}
    )

