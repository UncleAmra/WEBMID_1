import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User, Product, GroupBuying, Order
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:thisisme10@localhost:5432/groupbuy_system')

# Render compatibility: replace postgres:// with postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'groupbuy_secret_key_change_in_production')

db.init_app(app)


# --- HELPER FUNCTIONS ---
def login_required(f):
    """裝飾器：要求用戶登入"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """裝飾器：要求管理員權限"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('需要管理員權限', 'danger')
            return redirect(url_for('browse'))
        return f(*args, **kwargs)
    return decorated_function


# --- AUTHENTICATION ROUTES ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    """用戶註冊"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        # 檢查用戶是否已存在
        if User.query.filter_by(username=username).first():
            flash('用戶名已存在', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email 已被註冊', 'danger')
            return redirect(url_for('register'))
        
        # 創建新用戶
        new_user = User(username=username, email=email, name=name)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('註冊成功！請登入', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """用戶登入"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['name'] = user.name
            session['role'] = user.role
            
            flash(f'歡迎回來，{user.name}！', 'success')
            return redirect(url_for('browse'))
        else:
            flash('用戶名或密碼錯誤', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """用戶登出"""
    session.clear()
    flash('已成功登出', 'info')
    return redirect(url_for('login'))


# --- MAIN ROUTES ---
@app.route('/')
def index():
    """首頁 - 重定向到瀏覽頁面"""
    return redirect(url_for('browse'))


@app.route('/browse')
def browse():
    """瀏覽團購列表"""
    # 獲取所有進行中的團購
    active_groups = GroupBuying.query.filter_by(status='ACTIVE').order_by(GroupBuying.created_at.desc()).all()
    
    # 更新過期的團購狀態
    for group in active_groups:
        if group.is_expired:
            if group.current_quantity >= group.target_quantity:
                group.status = 'SUCCESS'
            else:
                group.status = 'FAILED'
            db.session.commit()
    
    # 重新獲取活躍團購
    active_groups = GroupBuying.query.filter_by(status='ACTIVE').order_by(GroupBuying.created_at.desc()).all()
    
    return render_template('browse.html', groups=active_groups)


@app.route('/group/<int:group_id>')
def group_detail(group_id):
    """團購詳情頁面"""
    group = GroupBuying.query.get_or_404(group_id)
    
    # 獲取該團購的所有訂單
    orders = Order.query.filter_by(group_buying_id=group_id).all()
    
    return render_template('group_detail.html', group=group, orders=orders)


@app.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    """開團 - 創建新團購"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        product_mode = request.form.get('product_mode', 'existing')
        target_quantity = int(request.form.get('target_quantity'))
        deadline_str = request.form.get('deadline')
        
        # 解析截止日期
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('日期格式錯誤', 'danger')
            return redirect(url_for('create_group'))
        
        # 處理商品
        product_id = None
        
        if product_mode == 'custom':
            # 創建新商品
            custom_name = request.form.get('custom_product_name')
            custom_price = float(request.form.get('custom_product_price'))
            custom_category = request.form.get('custom_product_category') or '其他'
            custom_desc = request.form.get('custom_product_desc') or ''
            
            # 檢查必填欄位
            if not custom_name or not custom_price:
                flash('請填寫商品名稱和價格', 'danger')
                return redirect(url_for('create_group'))
            
            # 創建新商品
            new_product = Product(
                name=custom_name,
                price=custom_price,
                category=custom_category,
                description=custom_desc,
                stock_quantity=999,  # 預設庫存
                image_url='https://picsum.photos/400/300?random=' + str(datetime.now().timestamp())
            )
            
            db.session.add(new_product)
            db.session.flush()  # 獲取 product_id
            product_id = new_product.id
            
        else:
            # 使用現有商品
            product_id = request.form.get('product_id')
            if not product_id:
                flash('請選擇商品', 'danger')
                return redirect(url_for('create_group'))
        
        # 創建團購
        new_group = GroupBuying(
            name=name,
            description=description,
            product_id=product_id,
            leader_id=session['user_id'],
            target_quantity=target_quantity,
            deadline=deadline
        )
        
        db.session.add(new_group)
        db.session.commit()
        
        flash('團購創建成功！', 'success')
        return redirect(url_for('group_detail', group_id=new_group.id))
    
    # GET 請求 - 顯示創建表單
    products = Product.query.all()
    return render_template('create_group.html', products=products)


@app.route('/join_group/<int:group_id>', methods=['POST'])
@login_required
def join_group(group_id):
    """跟團 - 加入團購"""
    group = GroupBuying.query.get_or_404(group_id)
    
    # 檢查團購狀態
    if group.status != 'ACTIVE':
        flash('此團購已關閉', 'warning')
        return redirect(url_for('group_detail', group_id=group_id))
    
    if group.is_expired:
        flash('此團購已過期', 'warning')
        return redirect(url_for('group_detail', group_id=group_id))
    
    # 獲取數量
    quantity = int(request.form.get('quantity', 1))
    
    # 檢查數量是否超過剩餘名額
    if quantity > group.remaining_slots:
        flash(f'剩餘名額不足！僅剩 {group.remaining_slots} 個名額', 'warning')
        return redirect(url_for('group_detail', group_id=group_id))
    
    # 計算總價
    total_price = group.product.price * quantity
    
    # 創建訂單
    new_order = Order(
        user_id=session['user_id'],
        group_buying_id=group_id,
        quantity=quantity,
        total_price=total_price
    )
    
    db.session.add(new_order)
    
    # 更新團購當前數量
    group.current_quantity += quantity
    
    # 檢查是否達到目標
    if group.current_quantity >= group.target_quantity:
        group.status = 'SUCCESS'
    
    db.session.commit()
    
    flash(f'成功加入團購！訂購 {quantity} 件，總計 ${total_price:.2f}', 'success')
    return redirect(url_for('my_orders'))


@app.route('/my-orders')
@login_required
def my_orders():
    """我的訂單 - 查看個人訂單歷史"""
    orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)


# --- ADMIN ROUTES ---
@app.route('/admin')
@login_required
def admin_dashboard():
    """後台管理 - 查看所有團購"""
    # 檢查是否為管理員或團長
    user = User.query.get(session['user_id'])
    
    if user.role == 'admin':
        # 管理員可以看到所有團購
        all_groups = GroupBuying.query.order_by(GroupBuying.created_at.desc()).all()
    else:
        # 一般用戶只能看到自己創建的團購
        all_groups = GroupBuying.query.filter_by(leader_id=session['user_id']).order_by(GroupBuying.created_at.desc()).all()
    
    # 統計數據
    total_groups = len(all_groups)
    active_groups = len([g for g in all_groups if g.status == 'ACTIVE'])
    success_groups = len([g for g in all_groups if g.status == 'SUCCESS'])
    
    return render_template('admin.html', 
                         groups=all_groups,
                         total_groups=total_groups,
                         active_groups=active_groups,
                         success_groups=success_groups)


@app.route('/admin/delete_group/<int:group_id>', methods=['POST'])
@login_required
def delete_group(group_id):
    """刪除團購"""
    group = GroupBuying.query.get_or_404(group_id)
    
    # 檢查權限
    user = User.query.get(session['user_id'])
    if user.role != 'admin' and group.leader_id != session['user_id']:
        flash('你沒有權限刪除此團購', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    db.session.delete(group)
    db.session.commit()
    
    flash('團購已刪除', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/close_group/<int:group_id>', methods=['POST'])
@login_required
def close_group(group_id):
    """關閉團購"""
    group = GroupBuying.query.get_or_404(group_id)
    
    # 檢查權限
    user = User.query.get(session['user_id'])
    if user.role != 'admin' and group.leader_id != session['user_id']:
        flash('你沒有權限關閉此團購', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    group.status = 'CLOSED'
    db.session.commit()
    
    flash('團購已關閉', 'success')
    return redirect(url_for('admin_dashboard'))


# --- PRODUCT MANAGEMENT ---
@app.route('/admin/products')
@admin_required
def manage_products():
    """管理商品"""
    products = Product.query.all()
    return render_template('manage_products.html', products=products)


@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    """添加商品"""
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        stock_quantity = int(request.form.get('stock_quantity'))
        description = request.form.get('description')
        image_url = request.form.get('image_url')
        
        new_product = Product(
            name=name,
            price=price,
            stock_quantity=stock_quantity,
            description=description,
            image_url=image_url
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        flash('商品添加成功！', 'success')
        return redirect(url_for('manage_products'))
    
    return render_template('add_product.html')


# --- DATABASE INITIALIZATION ---
@app.route('/init-db')
def init_db():
    """初始化數據庫"""
    with app.app_context():
        db.create_all()
        
        # 創建管理員帳號（如果不存在）
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@groupbuy.com',
                name='系統管理員',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # 創建測試商品（如果不存在）
        if Product.query.count() == 0:
            test_products = [
                Product(
                    name='iPhone 15 Pro',
                    price=999.99,
                    stock_quantity=50,
                    description='最新款 iPhone，搭載 A17 Pro 晶片',
                    image_url='https://images.unsplash.com/photo-1592286927505-2fd3dbf7a4d1?w=800'
                ),
                Product(
                    name='MacBook Air M3',
                    price=1299.99,
                    stock_quantity=30,
                    description='輕薄筆電，M3 晶片加持',
                    image_url='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800'
                ),
                Product(
                    name='AirPods Pro',
                    price=249.99,
                    stock_quantity=100,
                    description='主動降噪無線耳機',
                    image_url='https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=800'
                )
            ]
            db.session.add_all(test_products)
        
        db.session.commit()
    
    return "Database initialized successfully! <a href='/'>Go to home page</a>"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005)
