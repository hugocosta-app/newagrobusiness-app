from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256)) # Increased length for stronger hashes
    is_admin = db.Column(db.Boolean, default=False)
    nickname = db.Column(db.String(64), nullable=True) # New field for nickname

    # Relationships (add later as needed for orders, expenses, etc.)
    # orders = db.relationship("Order", backref="seller", lazy="dynamic")
    # expenses = db.relationship("Expense", backref="seller", lazy="dynamic")
    # visits = db.relationship("Visit", backref="seller", lazy="dynamic")
    # agenda_entries = db.relationship("AgendaEntry", backref="seller", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    

def check_password(self, password):
    
    result = check_password_hash(self.password_hash, password)
    return result




    def __repr__(self):
        return f"<User {self.username}>"

    @staticmethod
    def create_user(username, email, password, is_admin=False, nickname=None):
        user = User(username=username, email=email, is_admin=is_admin, nickname=nickname)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

