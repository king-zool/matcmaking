from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import json
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Production-ready configuration with environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'afcfta-trade-matchmaker-2025')

# Database configuration - supports PostgreSQL and SQLite
database_url = os.environ.get('DATABASE_URL', 'sqlite:///afcfta_trades.db')
# Fix for Heroku postgres:// to postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Add JSON filter for templates
@app.template_filter('from_json')
def from_json_filter(value):
    if value:
        try:
            return json.loads(value)
        except:
            return []
    return []

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'importer', 'exporter', or 'admin'
    country = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    # Company Profile Fields
    business_description = db.Column(db.Text)
    products_services = db.Column(db.Text)  # JSON string of product categories
    annual_volume = db.Column(db.String(50))
    company_size = db.Column(db.String(50))
    certifications = db.Column(db.Text)
    languages = db.Column(db.Text)
    preferred_countries = db.Column(db.Text)  # JSON string of countries
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TradeMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    compatibility_score = db.Column(db.Float, nullable=False)
    match_reasons = db.Column(db.Text)  # JSON string of matching criteria
    status = db.Column(db.String(20), default='pending')  # pending, contacted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdminSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # certificate, permit, contract, etc.
    document_name = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(500))
    verification_status = db.Column(db.String(20), default='pending')  # pending, verified, rejected
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class TradeInsight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commodity_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Float)
    price_change = db.Column(db.Float)  # percentage change
    volume_traded = db.Column(db.Float)
    source_country = db.Column(db.String(50))
    destination_country = db.Column(db.String(50))
    market_trend = db.Column(db.String(20))  # rising, falling, stable
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class FinanceCalculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calculation_type = db.Column(db.String(50))  # working_capital, trade_finance, etc.
    parameters = db.Column(db.Text)  # JSON parameters
    result = db.Column(db.Text)  # JSON result
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# AfCFTA Countries Data
AFCFTA_COUNTRIES = [
    'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon',
    'Cape Verde', 'Central African Republic', 'Chad', 'Comoros', 'Congo', 'Democratic Republic of Congo',
    'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon',
    'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho',
    'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius',
    'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe',
    'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan',
    'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
]

# Active GTI Countries (priority markets)
GTI_COUNTRIES = ['Ghana', 'Kenya', 'Rwanda', 'Tanzania', 'Mauritius', 'Egypt', 'Cameroon', 'South Africa']

# Product Categories (HS Code based)
PRODUCT_CATEGORIES = {
    'agricultural_products': 'Agricultural Products & Food',
    'textiles_clothing': 'Textiles & Clothing',
    'machinery_equipment': 'Machinery & Equipment',
    'electronics_technology': 'Electronics & Technology',
    'chemicals_pharmaceuticals': 'Chemicals & Pharmaceuticals',
    'metals_minerals': 'Metals & Minerals',
    'automotive_transport': 'Automotive & Transport Equipment',
    'wood_paper': 'Wood & Paper Products',
    'plastics_rubber': 'Plastics & Rubber',
    'construction_materials': 'Construction Materials',
    'energy_petroleum': 'Energy & Petroleum Products',
    'handicrafts_arts': 'Handicrafts & Arts',
    'services_consulting': 'Services & Consulting'
}

class AIMatchmaker:
    """AI-powered trade matchmaking engine for AfCFTA"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.scaler = StandardScaler()
    
    def calculate_compatibility(self, user1, user2):
        """Calculate compatibility score between two users"""
        if user1.user_type == user2.user_type:
            return 0.0  # Same type users don't match
        
        score = 0.0
        reasons = []
        
        # 1. Geographic Compatibility (30% weight)
        geo_score = self._calculate_geographic_score(user1, user2)
        score += geo_score * 0.3
        if geo_score > 0.7:
            reasons.append(f"Strong geographic alignment")
        
        # 2. Product/Service Compatibility (40% weight)
        product_score = self._calculate_product_score(user1, user2)
        score += product_score * 0.4
        if product_score > 0.6:
            reasons.append(f"Product category match")
        
        # 3. Business Size Compatibility (15% weight)
        size_score = self._calculate_size_score(user1, user2)
        score += size_score * 0.15
        
        # 4. Language Compatibility (10% weight)
        lang_score = self._calculate_language_score(user1, user2)
        score += lang_score * 0.1
        
        # 5. GTI Priority Boost (5% weight)
        gti_score = self._calculate_gti_score(user1, user2)
        score += gti_score * 0.05
        if gti_score > 0:
            reasons.append("Both in AfCFTA Guided Trade Initiative")
        
        return min(score, 1.0), reasons
    
    def _calculate_geographic_score(self, user1, user2):
        """Calculate geographic compatibility"""
        score = 0.0
        
        # Check if users are from different countries (basic requirement)
        if user1.country != user2.country:
            score += 0.3
        
        # Check preferred countries
        try:
            user1_prefs = json.loads(user1.preferred_countries or '[]')
            user2_prefs = json.loads(user2.preferred_countries or '[]')
            
            if user2.country in user1_prefs:
                score += 0.4
            if user1.country in user2_prefs:
                score += 0.4
        except:
            pass
        
        return min(score, 1.0)
    
    def _calculate_product_score(self, user1, user2):
        """Calculate product/service compatibility"""
        try:
            user1_products = set(json.loads(user1.products_services or '[]'))
            user2_products = set(json.loads(user2.products_services or '[]'))
            
            if not user1_products or not user2_products:
                return 0.3  # Default score if no product data
            
            # Calculate intersection
            intersection = len(user1_products.intersection(user2_products))
            union = len(user1_products.union(user2_products))
            
            if union > 0:
                return intersection / union
            
        except:
            pass
        
        return 0.3
    
    def _calculate_size_score(self, user1, user2):
        """Calculate business size compatibility"""
        size_mapping = {
            'micro': 1, 'small': 2, 'medium': 3, 'large': 4, 'enterprise': 5
        }
        
        try:
            size1 = size_mapping.get(user1.company_size, 3)
            size2 = size_mapping.get(user2.company_size, 3)
            
            # Compatible if within 2 levels
            diff = abs(size1 - size2)
            return max(0, 1 - diff / 4)
        except:
            return 0.7  # Default compatibility
    
    def _calculate_language_score(self, user1, user2):
        """Calculate language compatibility"""
        try:
            lang1 = set((user1.languages or 'english').lower().split(','))
            lang2 = set((user2.languages or 'english').lower().split(','))
            
            if lang1.intersection(lang2):
                return 1.0
            else:
                return 0.5  # English default
        except:
            return 0.7
    
    def _calculate_gti_score(self, user1, user2):
        """Boost score for GTI countries"""
        if user1.country in GTI_COUNTRIES and user2.country in GTI_COUNTRIES:
            return 1.0
        elif user1.country in GTI_COUNTRIES or user2.country in GTI_COUNTRIES:
            return 0.5
        return 0.0
    
    def find_matches(self, user_id, limit=10):
        """Find top matches for a user"""
        current_user = User.query.get(user_id)
        if not current_user:
            return []
        
        # Get potential matches (opposite user type)
        opposite_type = 'exporter' if current_user.user_type == 'importer' else 'importer'
        potential_matches = User.query.filter(
            User.user_type == opposite_type,
            User.id != user_id
        ).all()
        
        matches = []
        for potential_match in potential_matches:
            score, reasons = self.calculate_compatibility(current_user, potential_match)
            if score > 0.3:  # Minimum threshold
                matches.append({
                    'user': potential_match,
                    'score': score,
                    'reasons': reasons
                })
        
        # Sort by score and return top matches
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:limit]

# Initialize AI Matchmaker
ai_matcher = AIMatchmaker()

# Admin Helper Functions
def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    """Decorator to require user login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_active:
            session.clear()
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def log_admin_action(admin_id, action, target_user_id=None, details=None):
    """Log admin actions for audit trail"""
    log = AdminLog(
        admin_id=admin_id,
        action=action,
        target_user_id=target_user_id,
        details=details
    )
    db.session.add(log)
    db.session.commit()

def get_platform_metrics():
    """Get platform analytics metrics"""
    total_users = User.query.filter(User.user_type != 'admin').count()
    total_importers = User.query.filter_by(user_type='importer').count()
    total_exporters = User.query.filter_by(user_type='exporter').count()
    verified_users = User.query.filter(User.is_verified == True, User.user_type != 'admin').count()
    active_users = User.query.filter(User.is_active == True, User.user_type != 'admin').count()
    total_matches = TradeMatch.query.count()
    successful_connections = TradeMatch.query.filter_by(status='contacted').count()
    
    # Country distribution
    country_stats = db.session.query(User.country, db.func.count(User.id)).filter(User.user_type != 'admin').group_by(User.country).all()
    
    # GTI vs Non-GTI users
    gti_users = User.query.filter(User.country.in_(GTI_COUNTRIES), User.user_type != 'admin').count()
    
    return {
        'total_users': total_users,
        'total_importers': total_importers,
        'total_exporters': total_exporters,
        'verified_users': verified_users,
        'active_users': active_users,
        'total_matches': total_matches,
        'successful_connections': successful_connections,
        'country_stats': country_stats,
        'gti_users': gti_users,
        'verification_rate': (verified_users / total_users * 100) if total_users > 0 else 0,
        'success_rate': (successful_connections / total_matches * 100) if total_matches > 0 else 0
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html', afcfta_countries=AFCFTA_COUNTRIES, gti_countries=GTI_COUNTRIES)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        # Check if user exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Email already registered'})
        
        # Create new user
        user = User(
            email=data['email'],
            company_name=data['company_name'],
            user_type=data['user_type'],
            country=data['country'],
            contact_person=data.get('contact_person', ''),
            phone=data.get('phone', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('register.html', 
                         afcfta_countries=AFCFTA_COUNTRIES, 
                         product_categories=PRODUCT_CATEGORIES)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']):
            if not user.is_active:
                return jsonify({'success': False, 'message': 'Account has been deactivated'})
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            session['user_id'] = user.id
            
            # Redirect admin users to admin dashboard
            if user.is_admin:
                return jsonify({'success': True, 'message': 'Login successful', 'redirect': '/admin'})
            else:
                return jsonify({'success': True, 'message': 'Login successful', 'redirect': '/dashboard'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Update profile
        user.business_description = data.get('business_description', '')
        user.products_services = json.dumps(data.get('products_services', []))
        user.annual_volume = data.get('annual_volume', '')
        user.company_size = data.get('company_size', '')
        user.certifications = data.get('certifications', '')
        user.languages = data.get('languages', '')
        user.preferred_countries = json.dumps(data.get('preferred_countries', []))
        user.website = data.get('website', '')
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    
    # Parse JSON fields for display
    try:
        user.products_services_list = json.loads(user.products_services or '[]')
        user.preferred_countries_list = json.loads(user.preferred_countries or '[]')
    except:
        user.products_services_list = []
        user.preferred_countries_list = []
    
    return render_template('profile.html', 
                         user=user, 
                         afcfta_countries=AFCFTA_COUNTRIES,
                         product_categories=PRODUCT_CATEGORIES)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # Get AI-powered matches
    matches = ai_matcher.find_matches(user.id)
    
    # Get statistics
    total_users = User.query.count()
    importers = User.query.filter_by(user_type='importer').count()
    exporters = User.query.filter_by(user_type='exporter').count()
    gti_users = User.query.filter(User.country.in_(GTI_COUNTRIES)).count()
    
    stats = {
        'total_users': total_users,
        'importers': importers,
        'exporters': exporters,
        'gti_users': gti_users
    }
    
    return render_template('dashboard.html', 
                         user=user, 
                         matches=matches, 
                         stats=stats,
                         product_categories=PRODUCT_CATEGORIES)

@app.route('/api/matches')
def get_matches():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'})
    
    matches = ai_matcher.find_matches(session['user_id'])
    
    # Convert to JSON-serializable format
    result = []
    for match in matches:
        user = match['user']
        try:
            products = json.loads(user.products_services or '[]')
        except:
            products = []
        
        result.append({
            'id': user.id,
            'company_name': user.company_name,
            'country': user.country,
            'user_type': user.user_type,
            'business_description': user.business_description or '',
            'products': products,
            'compatibility_score': round(match['score'] * 100, 1),
            'match_reasons': match['reasons'],
            'contact_person': user.contact_person or '',
            'email': user.email,
            'phone': user.phone or '',
            'website': user.website or ''
        })
    
    return jsonify(result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with overview metrics"""
    metrics = get_platform_metrics()
    recent_users = User.query.filter(User.user_type != 'admin').order_by(User.created_at.desc()).limit(10).all()
    recent_matches = db.session.query(TradeMatch, User.alias('user1'), User.alias('user2')).join(
        User.alias('user1'), TradeMatch.user1_id == User.alias('user1').id
    ).join(
        User.alias('user2'), TradeMatch.user2_id == User.alias('user2').id
    ).order_by(TradeMatch.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         metrics=metrics, 
                         recent_users=recent_users, 
                         recent_matches=recent_matches)

@app.route('/admin/users')
@admin_required
def admin_users():
    """User management interface"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    filter_type = request.args.get('type', 'all', type=str)
    filter_status = request.args.get('status', 'all', type=str)
    
    query = User.query.filter(User.user_type != 'admin')
    
    if search:
        query = query.filter(
            (User.company_name.contains(search)) |
            (User.email.contains(search)) |
            (User.country.contains(search))
        )
    
    if filter_type != 'all':
        query = query.filter_by(user_type=filter_type)
    
    if filter_status == 'verified':
        query = query.filter_by(is_verified=True)
    elif filter_status == 'unverified':
        query = query.filter_by(is_verified=False)
    elif filter_status == 'active':
        query = query.filter_by(is_active=True)
    elif filter_status == 'inactive':
        query = query.filter_by(is_active=False)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users, search=search, 
                         filter_type=filter_type, filter_status=filter_status)

@app.route('/admin/user/<int:user_id>')
@admin_required
def admin_user_detail(user_id):
    """Detailed user view for admin"""
    user = User.query.get_or_404(user_id)
    user_matches = TradeMatch.query.filter(
        (TradeMatch.user1_id == user_id) | (TradeMatch.user2_id == user_id)
    ).order_by(TradeMatch.created_at.desc()).all()
    
    admin_logs = AdminLog.query.filter_by(target_user_id=user_id).order_by(AdminLog.timestamp.desc()).limit(10).all()
    
    return render_template('admin/user_detail.html', user=user, 
                         user_matches=user_matches, admin_logs=admin_logs)

@app.route('/admin/user/<int:user_id>/action', methods=['POST'])
@admin_required
def admin_user_action(user_id):
    """Perform actions on users (verify, suspend, etc.)"""
    user = User.query.get_or_404(user_id)
    action = request.json.get('action')
    admin_id = session['user_id']
    
    if action == 'verify':
        user.is_verified = True
        log_admin_action(admin_id, 'VERIFY_USER', user_id, f'Verified user {user.company_name}')
        
    elif action == 'unverify':
        user.is_verified = False
        log_admin_action(admin_id, 'UNVERIFY_USER', user_id, f'Removed verification from {user.company_name}')
        
    elif action == 'activate':
        user.is_active = True
        log_admin_action(admin_id, 'ACTIVATE_USER', user_id, f'Activated user {user.company_name}')
        
    elif action == 'deactivate':
        user.is_active = False
        log_admin_action(admin_id, 'DEACTIVATE_USER', user_id, f'Deactivated user {user.company_name}')
        
    else:
        return jsonify({'success': False, 'message': 'Invalid action'})
    
    db.session.commit()
    return jsonify({'success': True, 'message': f'User {action}d successfully'})

@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    """Analytics dashboard"""
    metrics = get_platform_metrics()
    
    # Monthly registration trends
    monthly_registrations = db.session.query(
        db.func.strftime('%Y-%m', User.created_at).label('month'),
        db.func.count(User.id).label('count')
    ).filter(User.user_type != 'admin').group_by(
        db.func.strftime('%Y-%m', User.created_at)
    ).order_by('month').all()
    
    # Match success by country
    country_matches = db.session.query(
        User.country,
        db.func.count(TradeMatch.id).label('matches')
    ).join(TradeMatch, User.id == TradeMatch.user1_id).group_by(User.country).all()
    
    # Product category distribution
    all_users = User.query.filter(User.user_type != 'admin').all()
    product_distribution = {}
    for user in all_users:
        if user.products_services:
            try:
                products = json.loads(user.products_services)
                for product in products:
                    if product in product_distribution:
                        product_distribution[product] += 1
                    else:
                        product_distribution[product] = 1
            except:
                continue
    
    return render_template('admin/analytics.html', 
                         metrics=metrics,
                         monthly_registrations=monthly_registrations,
                         country_matches=country_matches,
                         product_distribution=product_distribution)

@app.route('/admin/matches')
@admin_required
def admin_matches():
    """Match monitoring"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all', type=str)
    
    query = db.session.query(TradeMatch, User.alias('user1'), User.alias('user2')).join(
        User.alias('user1'), TradeMatch.user1_id == User.alias('user1').id
    ).join(
        User.alias('user2'), TradeMatch.user2_id == User.alias('user2').id
    )
    
    if status_filter != 'all':
        query = query.filter(TradeMatch.status == status_filter)
    
    matches = query.order_by(TradeMatch.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Match statistics
    match_stats = {
        'total': TradeMatch.query.count(),
        'pending': TradeMatch.query.filter_by(status='pending').count(),
        'contacted': TradeMatch.query.filter_by(status='contacted').count(),
        'rejected': TradeMatch.query.filter_by(status='rejected').count()
    }
    
    return render_template('admin/matches.html', matches=matches, 
                         match_stats=match_stats, status_filter=status_filter)

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    """Platform settings management"""
    if request.method == 'POST':
        settings_data = request.json
        admin_id = session['user_id']
        
        for key, value in settings_data.items():
            setting = AdminSettings.query.filter_by(setting_key=key).first()
            if setting:
                setting.setting_value = str(value)
                setting.updated_at = datetime.utcnow()
                setting.updated_by = admin_id
            else:
                setting = AdminSettings(
                    setting_key=key,
                    setting_value=str(value),
                    updated_by=admin_id
                )
                db.session.add(setting)
        
        db.session.commit()
        log_admin_action(admin_id, 'UPDATE_SETTINGS', None, f'Updated platform settings')
        
        return jsonify({'success': True, 'message': 'Settings updated successfully'})
    
    # Get current settings
    settings = {}
    all_settings = AdminSettings.query.all()
    for setting in all_settings:
        settings[setting.setting_key] = setting.setting_value
    
    # Default settings if not set
    default_settings = {
        'platform_name': 'AfCFTA Trade Matchmaker',
        'min_match_score': '0.3',
        'max_matches_per_user': '10',
        'require_verification': 'true',
        'enable_gti_priority': 'true',
        'maintenance_mode': 'false'
    }
    
    for key, default_value in default_settings.items():
        if key not in settings:
            settings[key] = default_value
    
    return render_template('admin/settings.html', settings=settings)

@app.route('/admin/logs')
@admin_required
def admin_logs():
    """Admin activity logs"""
    page = request.args.get('page', 1, type=int)
    action_filter = request.args.get('action', 'all', type=str)
    
    query = db.session.query(AdminLog, User).join(User, AdminLog.admin_id == User.id)
    
    if action_filter != 'all':
        query = query.filter(AdminLog.action.contains(action_filter.upper()))
    
    logs = query.order_by(AdminLog.timestamp.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('admin/logs.html', logs=logs, action_filter=action_filter)

# ==================== ENHANCED FEATURES ====================

@app.route('/intelligence')
@login_required
def trade_intelligence():
    """AI-Powered Trade Intelligence Dashboard"""
    # Get current trade insights
    insights = TradeInsight.query.order_by(TradeInsight.last_updated.desc()).limit(20).all()
    
    # Get platform metrics for dashboard
    metrics = get_platform_metrics()
    
    return render_template('trade_intelligence.html', insights=insights, metrics=metrics)

@app.route('/intelligence/update', methods=['POST'])
@login_required
def update_trade_intelligence():
    """Update trade intelligence data (simulated for demo)"""
    # Simulate real-time commodity price updates
    commodities = [
        {'name': 'Cocoa', 'price': 2450.50, 'change': 2.3},
        {'name': 'Coffee', 'price': 158.75, 'change': -1.2},
        {'name': 'Cotton', 'price': 1.25, 'change': 0.8},
        {'name': 'Cocoa Butter', 'price': 4120.25, 'change': 1.9},
        {'name': 'Gold', 'price': 1975.30, 'change': 0.5},
        {'name': 'Copper', 'price': 8920.15, 'change': -0.7},
        {'name': 'Crude Oil', 'price': 78.45, 'change': 1.1},
        {'name': 'Shea Butter', 'price': 2150.80, 'change': 3.2}
    ]
    
    updated_insights = []
    for commodity in commodities:
        insight = TradeInsight(
            commodity_name=commodity['name'],
            current_price=commodity['price'],
            price_change=commodity['change'],
            volume_traded=np.random.uniform(1000, 10000),
            source_country=np.random.choice(AFCFTA_COUNTRIES),
            destination_country=np.random.choice(AFCFTA_COUNTRIES),
            market_trend='rising' if commodity['change'] > 0 else 'falling'
        )
        db.session.add(insight)
        updated_insights.append({
            'name': commodity['name'],
            'price': commodity['price'],
            'change': commodity['change'],
            'trend': 'rising' if commodity['change'] > 0 else 'falling'
        })
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Trade intelligence updated successfully',
        'insights': updated_insights
    })

@app.route('/chat')
@login_required
def ai_chat():
    """AI Trade Assistant Chat Interface"""
    user_id = session['user_id']
    # Get recent chat history
    chat_history = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.timestamp.desc()).limit(50).all()
    
    return render_template('ai_chat.html', chat_history=chat_history)

@app.route('/chat/send', methods=['POST'])
@login_required
def send_chat_message():
    """Send message to AI Trade Assistant"""
    user_id = session['user_id']
    data = request.json
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'success': False, 'message': 'Message cannot be empty'})
    
    # AI Response Logic (simplified for demo)
    response = generate_ai_response(message, user_id)
    
    # Save to database
    chat_msg = ChatMessage(
        user_id=user_id,
        message=message,
        response=response
    )
    db.session.add(chat_msg)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': message,
        'response': response,
        'timestamp': chat_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })

def generate_ai_response(message, user_id):
    """Generate AI response based on user message"""
    message_lower = message.lower()
    
    # Greeting responses
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm your AI Trade Assistant for AfCFTA. I can help you with trade opportunities, market insights, document requirements, and financing options. What would you like to know?"
    
    # Market/Price inquiries
    if any(word in message_lower for word in ['price', 'market', 'commodity', 'cost']):
        return "I can help you with current commodity prices. Our trade intelligence shows cocoa trading at $2,450/ton, coffee at $158.75/kg, and cotton at $1.25/kg. Would you like specific market analysis for a particular commodity or country?"
    
    # Matchmaking help
    if any(word in message_lower for word in ['match', 'partner', 'buyer', 'seller', 'importer', 'exporter']):
        return "I can assist with finding trade partners! Based on your profile, I'll look for importers/exporters in complementary product categories. You can also update your profile with specific products and target countries to get better matches."
    
    # Document requirements
    if any(word in message_lower for word in ['document', 'certificate', 'permit', 'paperwork']):
        return "For AfCFTA trade, you may need: Certificate of Origin, Product certifications, Export permits, and quality certificates. Our document management system can help you track and verify these documents."
    
    # Financing options
    if any(word in message_lower for word in ['finance', 'loan', 'capital', 'funding', 'credit']):
        return "Trade financing options include: Letter of Credit, Trade Finance, Working Capital loans, and Export Credit. The trade finance calculator can help you determine the right financing structure for your transactions."
    
    # GTI guidance
    if any(word in message_lower for word in ['gti', 'guided trade', 'pilot']):
        return "The AfCFTA Guided Trade Initiative focuses on priority products between Ghana, Kenya, Rwanda, Tanzania, Mauritius, Egypt, Cameroon, and South Africa. This streamlines trade procedures and reduces tariffs significantly."
    
    # Default helpful response
    return f"Thanks for your question about '{message}'. I can help with trade matchmaking, market intelligence, document requirements, financing options, and AfCFTA regulations. Could you be more specific about what you'd like to know?"

@app.route('/documents')
@login_required
def document_management():
    """Document Management System"""
    user_id = session['user_id']
    documents = Document.query.filter_by(user_id=user_id).order_by(Document.uploaded_at.desc()).all()
    
    return render_template('documents.html', documents=documents)

@app.route('/documents/upload', methods=['POST'])
@login_required
def upload_document():
    """Upload and process trade documents"""
    user_id = session['user_id']
    data = request.json
    
    document = Document(
        user_id=user_id,
        document_type=data.get('document_type'),
        document_name=data.get('document_name'),
        verification_status='pending'
    )
    
    db.session.add(document)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Document uploaded successfully',
        'document_id': document.id
    })

@app.route('/documents/<int:doc_id>/verify', methods=['POST'])
@admin_required
def verify_document(doc_id):
    """Admin verification of documents"""
    document = Document.query.get_or_404(doc_id)
    admin_id = session['user_id']
    
    document.verification_status = 'verified'
    document.verified_at = datetime.utcnow()
    document.verified_by = admin_id
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Document verified successfully'
    })

@app.route('/finance')
@login_required
def finance_calculator():
    """Trade Finance Calculator"""
    user_id = session['user_id']
    calculations = FinanceCalculation.query.filter_by(user_id=user_id).order_by(FinanceCalculation.created_at.desc()).limit(10).all()
    
    return render_template('finance.html', calculations=calculations)

@app.route('/finance/calculate', methods=['POST'])
@login_required
def calculate_trade_finance():
    """Calculate trade financing options"""
    user_id = session['user_id']
    data = request.json
    
    calculation_type = data.get('type', 'working_capital')
    
    if calculation_type == 'working_capital':
        # Working Capital Calculation
        invoice_amount = float(data.get('invoice_amount', 0))
        payment_terms = int(data.get('payment_terms_days', 30))
        operating_cycle = float(data.get('operating_cycle_days', 60))
        
        # Calculate working capital requirement
        daily_sales = invoice_amount / 30
        working_capital_needed = daily_sales * operating_cycle
        
        # Financing options
        results = {
            'working_capital_needed': round(working_capital_needed, 2),
            'lending_rate': 8.5,  # Typical AfCFTA rate
            'interest_cost': round((working_capital_needed * 0.085 * payment_terms / 365), 2),
            'financing_options': [
                {'type': 'Invoice Financing', 'rate': 0.12, 'terms': '30-60 days'},
                {'type': 'Trade Credit', 'rate': 0.08, 'terms': 'Net 60'},
                {'type': 'Working Capital Loan', 'rate': 0.11, 'terms': '1-2 years'},
                {'type': 'Factoring', 'rate': 0.15, 'terms': 'Immediate'}
            ],
            'recommendation': 'Invoice Financing for quick access with competitive rates'
        }
        
    elif calculation_type == 'letter_of_credit':
        # Letter of Credit Calculation
        transaction_value = float(data.get('transaction_value', 0))
        countries_involved = data.get('countries', [])
        
        results = {
            'transaction_value': transaction_value,
            'lc_fee': round(transaction_value * 0.003, 2),  # 0.3% typical fee
            'processing_time': '5-10 business days',
            'requirements': [
                'Commercial Invoice',
                'Packing List',
                'Certificate of Origin',
                'Letter of Credit Application'
            ],
            'risk_level': 'Low - Bank guaranteed'
        }
    
    # Save calculation
    calc = FinanceCalculation(
        user_id=user_id,
        calculation_type=calculation_type,
        parameters=json.dumps(data),
        result=json.dumps(results)
    )
    db.session.add(calc)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'results': results,
        'calculation_id': calc.id
    })

# ==================== API ENDPOINTS ====================

@app.route('/api/commodity-prices')
def get_commodity_prices():
    """Get real-time commodity prices (simulated)"""
    # In production, this would connect to actual market data APIs
    prices = {
        'commodities': [
            {'name': 'Cocoa', 'price': 2450.50, 'change': 2.3, 'unit': 'USD/ton'},
            {'name': 'Coffee', 'price': 158.75, 'change': -1.2, 'unit': 'USD/kg'},
            {'name': 'Cotton', 'price': 1.25, 'change': 0.8, 'unit': 'USD/kg'},
            {'name': 'Gold', 'price': 1975.30, 'change': 0.5, 'unit': 'USD/oz'},
            {'name': 'Copper', 'price': 8920.15, 'change': -0.7, 'unit': 'USD/ton'}
        ],
        'currencies': [
            {'code': 'USD', 'rate': 1.0, 'name': 'US Dollar'},
            {'code': 'EUR', 'rate': 0.92, 'name': 'Euro'},
            {'code': 'GBP', 'rate': 0.79, 'name': 'British Pound'},
            {'code': 'GHS', 'rate': 12.5, 'name': 'Ghana Cedi'},
            {'code': 'NGN', 'rate': 800.0, 'name': 'Nigerian Naira'},
            {'code': 'KES', 'rate': 130.0, 'name': 'Kenyan Shilling'}
        ],
        'last_updated': datetime.utcnow().isoformat()
    }
    return jsonify(prices)

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)