from app import db
from datetime import datetime

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    expense_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    km_initial = db.Column(db.Float, nullable=True)
    km_final = db.Column(db.Float, nullable=True)
    km_total = db.Column(db.Float, nullable=True)
    receipt_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key to User (Seller)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def calculate_km_total(self):
        if self.km_initial is not None and self.km_final is not None and self.km_final >= self.km_initial:
            self.km_total = round(self.km_final - self.km_initial, 2)
        else:
            self.km_total = None

    def __repr__(self):
        return f"<Expense {self.id} by {self.seller.username} on {self.date}>"

