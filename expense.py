from app import db
from datetime import datetime

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    expense_type = db.Column(db.String(50), nullable=False) # e.g., combustível, pedagio, Refeições, Hotel, Diversos
    amount = db.Column(db.Float, nullable=False) # Added amount field, seems essential for expenses
    description = db.Column(db.Text, nullable=True) # Optional description
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False) # UF (e.g., SP, MG)
    km_initial = db.Column(db.Float, nullable=True)
    km_final = db.Column(db.Float, nullable=True)
    km_total = db.Column(db.Float, nullable=True) # Calculated: km_final - km_initial
    receipt_filename = db.Column(db.String(255), nullable=True) # Store filename of the uploaded receipt
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key to User (Seller)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    seller = db.relationship("User", backref=db.backref("expenses", lazy="dynamic"))

    def calculate_km_total(self):
        if self.km_initial is not None and self.km_final is not None and self.km_final >= self.km_initial:
            self.km_total = round(self.km_final - self.km_initial, 2)
        else:
            self.km_total = None # Or 0, depending on requirements

    def __repr__(self):
        return f"<Expense {self.id} by {self.seller.username} on {self.date}>"

