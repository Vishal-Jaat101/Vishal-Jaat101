import os
import json
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'store.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# allow CORS for API endpoints during frontend development
CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price_inr = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(800))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CustomDesign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300))
    name = db.Column(db.String(120))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.Text)
    total = db.Column(db.Integer)
    status = db.Column(db.String(50), default='Processing')
    delivery_start = db.Column(db.Date)
    delivery_end = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Admin password
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated

def seed_products():
    samples = [
        {'name': 'Urban Elite Hoodie', 'description': 'Premium heavyweight hoodie. Midnight colorway.', 'price_inr': 5499, 'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=1000&q=80'},
        {'name': 'Midnight Luxe Hoodie', 'description': 'Sleek silhouette with brushed interior.', 'price_inr': 4999, 'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?auto=format&fit=crop&w=1000&q=80'},
        {'name': 'Golden Hour Sweatshirt', 'description': 'Soft cotton sweatshirt with premium finish.', 'price_inr': 3999, 'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=1000&q=80'},
        {'name': 'Velmington Classic Hoodie', 'description': 'Everyday comfort with a refined look.', 'price_inr': 1499, 'image_url': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=1000&q=80'},
    ]
    for s in samples:
        p = Product(name=s['name'], description=s['description'], price_inr=s['price_inr'], image_url=s['image_url'])
        db.session.add(p)
    db.session.commit()

def create_tables():
    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            seed_products()

### HTML routes ###
@app.route('/')
def index():
    products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    return render_template('index.html', products=products, brand='Velmington')

@app.route('/shop')
def shop():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('shop.html', products=products, brand='Velmington')

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        rating = int(request.form.get('rating', 5))
        comment = request.form.get('comment', '')
        r = Review(product_id=product.id, rating=rating, comment=comment)
        db.session.add(r)
        db.session.commit()
        flash('Review added — thank you!', 'success')
        return redirect(url_for('product_detail', product_id=product.id))
    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()
    avg_rating = None
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
    return render_template('product.html', product=product, reviews=reviews, avg_rating=avg_rating, brand='Velmington')

@app.route('/custom', methods=['GET', 'POST'])
def custom_design():
    if request.method == 'POST':
        name = request.form.get('name')
        notes = request.form.get('notes')
        file = request.files.get('design')
        filename = None
        if file and file.filename:
            filename = datetime.utcnow().strftime('%Y%m%d%H%M%S_') + file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cd = CustomDesign(filename=filename, name=name, notes=notes)
        db.session.add(cd)
        db.session.commit()
        flash('Design submitted. Our team will contact you.', 'success')
        return redirect(url_for('custom_design'))
    designs = CustomDesign.query.order_by(CustomDesign.created_at.desc()).limit(12).all()
    return render_template('custom.html', designs=designs, brand='Velmington')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/lookbook')
def lookbook():
    products = Product.query.order_by(Product.created_at.desc()).limit(12).all()
    return render_template('lookbook.html', products=products, brand='Velmington')

@app.route('/coupons')
def coupons():
    coupons = [
        {'code': 'VEL10', 'desc': '10% off on hoodies', 'expires': '2026-12-31'},
        {'code': 'SHIPFREE', 'desc': 'Free shipping above ₹1999', 'expires': '2026-12-31'},
    ]
    return render_template('coupons.html', coupons=coupons, brand='Velmington')

@app.route('/about')
def about():
    return render_template('about.html', brand='Velmington')

### Cart / checkout / payment ###
@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if p:
            items.append({'product': p, 'qty': qty})
            total += p.price_inr * qty
    return render_template('cart.html', items=items, total=total, brand='Velmington')

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash('Added to cart', 'success')
    return redirect(url_for('shop'))

@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if p:
            items.append({'product': p, 'qty': qty})
            total += p.price_inr * qty
    return render_template('checkout.html', items=items, total=total, brand='Velmington')

@app.route('/payment', methods=['POST'])
def payment():
    cart = session.get('cart', {})
    if not cart:
        flash('Cart empty', 'info')
        return redirect(url_for('shop'))
    items = []
    total = 0
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if p:
            items.append({'id': p.id, 'name': p.name, 'qty': qty, 'price': p.price_inr})
            total += p.price_inr * qty
    today = date.today()
    start = today + timedelta(days=3)
    end = today + timedelta(days=4)
    order = Order(items=json.dumps(items), total=total, status='Paid', delivery_start=start, delivery_end=end)
    db.session.add(order)
    db.session.commit()
    session.pop('cart', None)
    return redirect(url_for('order_confirmation', order_id=order.id))

@app.route('/order/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    items = json.loads(order.items) if order.items else []
    return render_template('order_confirmation.html', order=order, items=items, brand='Velmington')

### Admin ###
@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    if request.method == 'POST':
        if 'add' in request.form:
            name = request.form.get('name')
            desc = request.form.get('description')
            price = int(request.form.get('price', 0))
            image_url = request.form.get('image_url')
            p = Product(name=name, description=desc, price_inr=price, image_url=image_url)
            db.session.add(p)
            db.session.commit()
            flash('Product added', 'success')
            return redirect(url_for('admin'))
        if 'remove' in request.form:
            pid = int(request.form.get('product_id'))
            p = Product.query.get(pid)
            if p:
                db.session.delete(p)
                db.session.commit()
                flash('Product removed', 'info')
            return redirect(url_for('admin'))
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin.html', products=products, brand='Velmington')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin'] = True
            flash('Logged in as admin', 'success')
            nxt = request.args.get('next') or url_for('admin')
            return redirect(nxt)
        else:
            flash('Invalid password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', brand='Velmington')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logged out', 'info')
    return redirect(url_for('index'))

### Simple chatbot stub ###
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    msg = data.get('message', '')
    if not msg:
        return jsonify({'reply': "Hi! Send a message."})
    if 'hello' in msg.lower():
        return jsonify({'reply': 'Hello! Welcome to Velmington. How can I help with hoodies today?'})
    if 'price' in msg.lower():
        return jsonify({'reply': 'Prices are in INR. Check the shop page for exact prices.'})
    return jsonify({'reply': f'I heard you say: "{msg}" — this is a demo chatbot.'})

### Lightweight JSON APIs ###
@app.route('/api/products')
def api_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    out = []
    for p in products:
        out.append({'id': p.id, 'name': p.name, 'description': p.description, 'price_inr': p.price_inr, 'image_url': p.image_url})
    return jsonify(out)

@app.route('/api/product/<int:pid>')
def api_product(pid):
    p = Product.query.get_or_404(pid)
    return jsonify({'id': p.id, 'name': p.name, 'description': p.description, 'price_inr': p.price_inr, 'image_url': p.image_url})

if __name__ == '__main__':
    create_tables()
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
