from app import db
from datetime import datetime

class AgendaEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.Time, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="Agendado")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key to User (Seller)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<AgendaEntry {self.id} for {self.seller.username} on {self.date}>"

