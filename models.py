from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """用戶表 - 儲存帳號資訊、名稱、email、密碼、角色"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='member')  # 'member' or 'leader'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    led_groups = db.relationship('GroupBuying', backref='leader', lazy=True, foreign_keys='GroupBuying.leader_id')
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """設置密碼（加密）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """驗證密碼"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Product(db.Model):
    """商品表 - 儲存商品名稱、價格、庫存數量、描述"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group_buyings = db.relationship('GroupBuying', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'


class GroupBuying(db.Model):
    """團購表 - 儲存團購名稱、描述、截止日期、團長、狀態"""
    __tablename__ = 'group_buying'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_quantity = db.Column(db.Integer, nullable=False)  # 目標數量
    current_quantity = db.Column(db.Integer, default=0)  # 當前數量
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='ACTIVE')  # ACTIVE, CLOSED, SUCCESS, FAILED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='group_buying', lazy=True, cascade='all, delete-orphan')
    
    @property
    def progress_percentage(self):
        """計算進度百分比"""
        if self.target_quantity == 0:
            return 0
        return min(int((self.current_quantity / self.target_quantity) * 100), 100)
    
    @property
    def remaining_slots(self):
        """計算剩餘名額"""
        return max(self.target_quantity - self.current_quantity, 0)
    
    @property
    def is_active(self):
        """檢查是否還在進行中"""
        return self.status == 'ACTIVE' and datetime.utcnow() < self.deadline
    
    @property
    def is_expired(self):
        """檢查是否已過期"""
        return datetime.utcnow() > self.deadline
    
    def __repr__(self):
        return f'<GroupBuying {self.name}>'


class Order(db.Model):
    """訂單表 - 記錄用戶訂單、數量、關聯團購、付款狀態"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_buying_id = db.Column(db.Integer, db.ForeignKey('group_buying.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='PENDING')  # PENDING, PAID, CANCELLED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Order {self.id}>'
