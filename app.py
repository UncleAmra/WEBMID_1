import os
from flask import Flask, render_template, request, redirect, url_for, session
from models import db, GroupBuy, Product
from datetime import datetime

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
# This looks for 'DATABASE_URL' on Render. If not found, it uses your local PostgreSQL.
# Note: Render URLs often start with 'postgres://', but SQLAlchemy requires 'postgresql://'
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:thisisme10@localhost:5432/groupbuy_pro')

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'hotel_booking_secret_key'

db.init_app(app)

# --- HOTEL CATALOG DATA ---
ROOM_DATA = {
    'Single Bed Room': {'price': 120.0, 'img': 'https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=800'},
    'Double Bed Room': {'price': 180.0, 'img': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800'},
    'Luxury Suite': {'price': 350.0, 'img': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800'},
    'Family Room': {'price': 280.0, 'img': 'https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800'}
}

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/marketplace')
def marketplace():
    active_pools = GroupBuy.query.filter_by(status="ACTIVE").all()
    return render_template('marketplace.html', pools=active_pools)

@app.route('/create', methods=['GET', 'POST'])
def create_pool():
    if request.method == 'POST':
        selected_type = request.form['room_type']
        room_info = ROOM_DATA[selected_type]

        new_room = Product(
            name=selected_type,
            base_price=room_info['price'],
            image_url=room_info['img']
        )
        db.session.add(new_room)
        db.session.commit()

        new_pool = GroupBuy(
            product_id=new_room.id,
            leader_name=request.form['leader'],
            target_qty=int(request.form['goal']),
            deadline=datetime.strptime(request.form['deadline'], '%Y-%m-%dT%H:%M'),
            description=request.form['description']
        )
        db.session.add(new_pool)
        db.session.commit()
        return redirect(url_for('marketplace'))
    
    return render_template('create.html', room_options=ROOM_DATA.keys())

@app.route('/join/<int:pool_id>', methods=['POST'])
def join_pool(pool_id):
    pool = GroupBuy.query.get_or_404(pool_id)
    qty = int(request.form.get('qty', 1))
    
    pool.current_qty += qty
    if pool.current_qty >= pool.target_qty:
        pool.status = "SUCCESS"
    
    db.session.commit()

    if 'my_bookings' not in session:
        session['my_bookings'] = []
    
    booking_entry = {
        'room_name': pool.product.name,
        'qty': qty,
        'price': pool.product.base_price,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    temp_list = session['my_bookings']
    temp_list.append(booking_entry)
    session['my_bookings'] = temp_list

    return redirect(url_for('my_bookings_page'))

@app.route('/my-bookings')
def my_bookings_page():
    bookings = session.get('my_bookings', [])
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/admin')
def admin_dashboard():
    all_pools = GroupBuy.query.all()
    return render_template('admin.html', pools=all_pools)

@app.route('/delete-pool/<int:pool_id>', methods=['POST'])
def delete_pool(pool_id):
    pool = GroupBuy.query.get_or_404(pool_id)
    db.session.delete(pool)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/init-db')
def init_db():
    with app.app_context():
        db.create_all()
    return "Database tables created successfully! Go back to the site."

if __name__ == "__main__":
    app.run(debug=True)