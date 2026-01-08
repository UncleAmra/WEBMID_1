from flask import Flask, render_template, request, redirect, url_for
from models import db, GroupBuy, Product
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:thisisme10@localhost:5432/groupbuy_pro'
db.init_app(app)

@app.route('/')
def landing_page():
    # The professional introduction page
    return render_template('index.html')

@app.route('/marketplace')
def marketplace():
    # Shows all active group buying pools
    active_pools = GroupBuy.query.filter_by(status="ACTIVE").all()
    return render_template('marketplace.html', pools=active_pools)

@app.route('/join/<int:pool_id>', methods=['POST'])
def join_pool(pool_id):
    pool = GroupBuy.query.get_or_404(pool_id)
    qty = int(request.form.get('qty'))
    pool.current_qty += qty # Accumulates orders
    
    if pool.current_qty >= pool.target_qty:
        pool.status = "SUCCESS" # Goal met logic
    
    db.session.commit()
    return redirect(url_for('marketplace'))

@app.route('/admin')
def admin_dashboard():
    # The "Control Center" for managing chaos
    all_pools = GroupBuy.query.all()
    return render_template('admin.html', pools=all_pools)
if __name__ == "__main__":
    app.run(debug=True)
