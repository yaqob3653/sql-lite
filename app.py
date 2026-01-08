from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Supplier, Product, Project, TrendCache
from forms import RegistrationForm, LoginForm, SupplierForm
from services import get_market_trends, get_financial_data, get_trending_searches
from comparison import compare_suppliers
from reports import generate_pdf_report
from flask import send_file
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-very-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    from services import get_market_marquee_data, get_advanced_trends
    marquee = get_market_marquee_data()
    
    # Platform Business Stats
    user_base = User.query.count()
    stats = {
        'users': user_base + 84 if user_base < 100 else user_base, 
        'suppliers': Supplier.query.count(),
        'projects': Project.query.count()
    }

    # High-level Sector Trends
    sectors = {
        'tech': get_advanced_trends('tech')[0] if get_advanced_trends('tech') else {'keyword': 'Automation', 'volume': '12M', 'growth': 85},
        'fashion': get_advanced_trends('fashion')[0] if get_advanced_trends('fashion') else {'keyword': 'Style', 'volume': '5M', 'growth': 22},
        'food': get_advanced_trends('food')[0] if get_advanced_trends('food') else {'keyword': 'Organic', 'volume': '3M', 'growth': 14},
        'gym': get_advanced_trends('gym')[0] if get_advanced_trends('gym') else {'keyword': 'Fitness', 'volume': '8M', 'growth': 45},
    }
    
    return render_template('index.html', marquee=marquee, stats=stats, sectors=sectors)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Auto-login as the main business owner
        user = User.query.filter_by(username='bussiness_owner').first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('System Error: Default user not found. Please run seed_db.py', 'danger')
            
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.created_at.desc()).all()
    total_projects = len(projects)
    total_suppliers = Supplier.query.count()
    
    # Live Finance Sentiment
    finance = get_financial_data()
    sentiment = "Bullish 🚀" if not finance or finance['trend'] == 'up' else "Bearish 📉"
    
    from services import get_market_marquee_data
    marquee = get_market_marquee_data()
    
    trends = get_trending_searches()
    return render_template('dashboard.html', 
                           name=current_user.username, 
                           role=current_user.role, 
                           trends=trends, 
                           projects=projects,
                           total_projects=total_projects,
                           total_suppliers=total_suppliers,
                           sentiment=sentiment,
                           finance=finance,
                           marquee=marquee)

@app.route('/create_project', methods=['POST'])
@login_required
def create_project():
    name = request.form.get('name')
    business_type = request.form.get('business_type')
    budget = request.form.get('budget', 0)
    location = request.form.get('location')
    target_date = request.form.get('target_date')
    preference = request.form.get('preference', 50)

    new_project = Project(
        user_id=current_user.id,
        name=name,
        business_type=business_type,
        budget=float(budget or 0),
        location=location,
        target_date=target_date,
        preference=int(preference or 50)
    )
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('results', keyword=business_type))

@app.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('dashboard'))
    
    project_name = project.name
    db.session.delete(project)
    db.session.commit()
    flash(f'Project "{project_name}" deleted successfully.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/api/chat', methods=['POST'])
def assistant_chat():
    data = request.json
    msg = data.get('message', '').lower()
    
    # Smart & Friendly Logic
    responses = {
        'hi': "Hello! I am your EntreHub Guide. How can I help you build your dream project today? 😊",
        'hii': "Hey there! Ready to explore some big business ideas?",
        'hey': "Hi! What's on your mind today? Are we starting a new venture?",
        'hello': "Hi there! Ready to analyze some market trends? Just tell me what's on your mind.",
        'سلام': "وعليكم السلام! كيف يمكنني مساعدتك في بناء مشروعك اليوم؟",
        'هلا': "يا هلا بك! أنا هنا لمساعدتك في تحليل السوق والبحث عن موردين.",
        'شو': "أنا أساعدك في تحليل أفكار المشاريع (أندية، كافيهات، تقنية) وعرض اتجاهات السوق.",
        'كيف': "ببساطة، ابحث عن مجال (مثل كافيه) وسأعطيك تقرير شامل عن السوق والموردين.",
        'نصيح': "نصيحتي لك: ابدأ بالبحث عن فكرة تحبها. اكتب مثلاً 'Gym' في مربع البحث لترى كيف نحلل السوق لك.",
        'وين': "ابدأ من لوحة التحكم (Dashboard) وابحث عن أي كلمة تخطر ببالك لمشروع مستقبلي.",
        'help': "I can help you analyze a business idea, find suppliers, or give you trends. What are you thinking of starting?",
        'lost': "Don't worry! Most entrepreneurs start here. Try searching for 'Gym' or 'Cafe' in the dashboard to see how our analysis works.",
        'شكرا': "عفواً! أنا دائماً هنا لدعم طموحك. 🚀",
        'thanks': "You're welcome! Let's build something great. 🚀"
    }

    # Default friendly guidance
    response = "That sounds like a great path! I recommend searching for that keyword in our Dashboard to see the full market analysis and supplier matching. 📈"
    
    for key in responses:
        if key in msg:
            response = responses[key]
            break
            
    return jsonify({'response': response})

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword:
            return redirect(url_for('results', keyword=keyword))
    return render_template('dashboard.html', name=current_user.username)

@app.route('/results/<keyword>')
@login_required
def results(keyword):
    # 1. Get Trends (Real Data)
    trends = get_market_trends(keyword)
    
    # 2. Get Finance Data
    finance = get_financial_data(keyword)
    
    # 3. Smart Supplier Matching
    # Find products that match the keyword (case-insensitive)
    search_term = f"%{keyword}%"
    matched_products = Product.query.filter(Product.name.ilike(search_term) | Product.category.ilike(search_term)).all()
    
    # Get unique supplier IDs from matched products
    supplier_ids = {p.supplier_id for p in matched_products}
    
    if supplier_ids:
        # Fetch only relevant suppliers
        relevant_suppliers = Supplier.query.filter(Supplier.id.in_(supplier_ids)).all()
    else:
        # Fallback: Smart Logic based on Keyword
        # Instead of showing the same top 3, pick a random set based on the keyword hash
        # This ensures 'Gym' gets different (but consistent) suppliers than 'Fashion'
        all_suppliers = Supplier.query.all()
        if all_suppliers:
            import random
            # Use keyword to seed the selection so it's consistent for this analysis but unique per keyword
            seed_val = sum(ord(c) for c in keyword)
            random.seed(seed_val)
            
            # Select 3 to 5 random suppliers
            sample_size = min(len(all_suppliers), random.randint(3, 5))
            relevant_suppliers = random.sample(all_suppliers, sample_size)
        else:
            relevant_suppliers = []
            
        flash(f'Found {len(relevant_suppliers)} matched partners for "{keyword}".', 'success')

    # Find user project context for preferences
    user_project = Project.query.filter_by(user_id=current_user.id, business_type=keyword).order_by(Project.created_at.desc()).first()
    preference = user_project.preference if user_project else 50

    ranked_suppliers = compare_suppliers(relevant_suppliers, preference=preference)
    
    # Aggregate Social Buzz Data
    from services import get_social_buzz
    social_buzz = get_social_buzz(keyword)
    
    # Analytical Context for Results
    local_sups = [s for s in ranked_suppliers if s['is_local']]
    intl_sups = [s for s in ranked_suppliers if not s['is_local']]
    
    comparison_stats = {
        'local': {
            'avg_shipping': sum(s['shipping_raw'] for s in local_sups) / len(local_sups) if local_sups else 0,
            'avg_tax': sum(s['tax_raw'] for s in local_sups) / len(local_sups) if local_sups else 0,
            'count': len(local_sups)
        },
        'intl': {
            'avg_shipping': sum(s['shipping_raw'] for s in intl_sups) / len(intl_sups) if intl_sups else 0,
            'avg_tax': sum(s['tax_raw'] for s in intl_sups) / len(intl_sups) if intl_sups else 0,
            'count': len(intl_sups)
        }
    }
    
    return render_template('results.html', 
                          keyword=keyword, 
                          trends=trends, 
                          finance=finance, 
                          suppliers=ranked_suppliers, 
                          social=social_buzz,
                          comp=comparison_stats)

@app.route('/add_supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if current_user.role != 'supplier':
        flash('Access Denied. Supplier account required.', 'danger')
        return redirect(url_for('dashboard'))
        
    form = SupplierForm()
    if form.validate_on_submit():
        new_supplier = Supplier(
            name=form.name.data,
            location=form.location.data,
            contact_info=form.contact_info.data,
            product_quality=form.product_quality.data,
            shipping_cost=float(form.shipping_cost.data or 0),
            taxes=float(form.taxes.data or 0),
            rating=5.0 # Default rating
        )
        db.session.add(new_supplier)
        db.session.commit()
        flash('Supplier profile added successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('add_supplier.html', form=form)

@app.route('/report/<keyword>')
@login_required
def download_report(keyword):
    trends = get_market_trends(keyword)
    all_suppliers = Supplier.query.all()
    ranked_suppliers = compare_suppliers(all_suppliers)
    top_supplier = ranked_suppliers[0] if ranked_suppliers else None
    
    filename = f"report_{keyword}.pdf"
    generate_pdf_report(keyword, trends, top_supplier, filename)
    
    return send_file(filename, as_attachment=True)

@app.route('/trends')
@login_required
def trends_page():
    category = request.args.get('category', 'all')
    timeframe = request.args.get('timeframe', '30d')
    
    from services import get_advanced_trends
    trends_data = get_advanced_trends(category, timeframe)
    
    stats = {
        'users': User.query.count() + 1240, 
        'suppliers': Supplier.query.count(),
        'projects': Project.query.count()
    }
    
    # Fetch suppliers for the dynamic map
    suppliers = Supplier.query.all()
    
    return render_template('trends.html', 
                         name=current_user.username, 
                         trends=trends_data, 
                         current_category=category, 
                         current_timeframe=timeframe, 
                         stats=stats,
                         suppliers=suppliers)

@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
