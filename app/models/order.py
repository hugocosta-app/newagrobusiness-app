from app import db
from datetime import datetime

# Association table for many-to-many relationship between Order and Product
# Using an association object to store extra data (quantity, discount)
class OrderItem(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Float, nullable=False)
    discount_applied = db.Column(db.Float, default=0.0)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product")

    def __repr__(self):
        return f"<OrderItem Order:{self.order_id} Product:{self.product_id} Qty:{self.quantity}>"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(150), nullable=False)
    customer_cnpj = db.Column(db.String(20), nullable=False, index=True)
    delivery_address = db.Column(db.Text, nullable=False)
    order_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(50), default="Pendente")

    # Foreign Key to User (Seller)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Relationship to OrderItem
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def calculate_total(self):
        total = 0
        for item in self.items:
            item_total = item.price_at_order * item.quantity
            discount_amount = item_total * (item.discount_applied / 100.0)
            total += item_total - discount_amount
        self.total_amount = round(total, 2)
        return self.total_amount

    def __repr__(self):
        return f"<Order {self.id} by {self.customer_name}>"

