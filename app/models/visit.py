from app import db
from datetime import datetime

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    customer_name = db.Column(db.String(150), nullable=False)
    customer_cnpj = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    highlights = db.Column(db.Text, nullable=True)
    observations = db.Column(db.Text, nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key to User (Seller)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Visit {self.id} to {self.customer_name} on {self.date}>"

