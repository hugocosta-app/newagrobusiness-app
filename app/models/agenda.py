from app import db
from datetime import date, datetime

class AgendaEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False, index=True)
    location = db.Column(db.String(200), nullable=False) # City, region, or specific address
    description = db.Column(db.Text, nullable=True) # Planned activities, clients, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign Key to User (Seller)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    seller = db.relationship("User", backref=db.backref("agenda_entries", lazy="dynamic"))

    def __repr__(self):
        return f"<AgendaEntry {self.id} for {self.seller.username} on {self.entry_date}>"

