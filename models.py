from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500))

class GroupBuy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    leader_name = db.Column(db.String(100), nullable=False)
    target_qty = db.Column(db.Integer, nullable=False)
    current_qty = db.Column(db.Integer, default=0)
    deadline = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text) # ADDED THIS to match your form
    status = db.Column(db.String(20), default="ACTIVE")
    
    product = db.relationship('Product', backref='pools')