from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    # Add other relevant fields like SKU, category, stock, etc. if needed
    # sku = db.Column(db.String(50), unique=True, nullable=True)
    # category = db.Column(db.String(50), index=True)
    # stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship back to OrderItem (optional, might be useful)
    # order_items = db.relationship("OrderItem", backref="product", lazy="dynamic")

    def __repr__(self):
        return f"<Product {self.name}>"

