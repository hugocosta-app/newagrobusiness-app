from app import db
from datetime import datetime

class VisitPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visit.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<VisitPhoto {self.filename} for Visit {self.visit_id}>"

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(150), nullable=False, index=True)
    visit_date = db.Column(db.Date, nullable=False, index=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False) # UF
    products_discussed = db.Column(db.Text, nullable=True) # Could be comma-separated or JSON
    summary = db.Column(db.Text, nullable=False)
    highlights = db.Column(db.Text, nullable=True)
    observations = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key to User (Seller)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    seller = db.relationship("User", backref=db.backref("visits", lazy="dynamic"))

    # Relationship to VisitPhoto (one-to-many)
    photos = db.relationship("VisitPhoto", backref="visit", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Visit {self.id} to {self.customer_name} on {self.visit_date}>"

