from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student') # student, supplier, admin
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100)) # local, global
    contact_info = db.Column(db.String(500))
    rating = db.Column(db.Float, default=0.0)
    product_quality = db.Column(db.String(50)) # High, Medium, Low
    shipping_cost = db.Column(db.Float)
    taxes = db.Column(db.Float)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    base_price = db.Column(db.Float)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(200), nullable=False)
    business_type = db.Column(db.String(100), nullable=False) # e.g. Gym, Cafe
    budget = db.Column(db.Float)
    location = db.Column(db.String(200))
    target_date = db.Column(db.String(100))
    preference = db.Column(db.Integer, default=50) # 0: Cheapest, 100: Best Quality
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def readiness_score(self):
        """Calculates real progress percentage based on filled data."""
        score = 0
        if self.name: score += 20
        if self.business_type: score += 20
        if self.budget and self.budget > 0: score += 20
        if self.location: score += 20
        if self.target_date: score += 20
        return score

class TrendCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100))
    data = db.Column(db.JSON)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
