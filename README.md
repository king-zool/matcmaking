# AfCFTA Trade Matchmaker MVP

🌍 **AI-Powered Trade Matching Platform for the African Continental Free Trade Area**

A sophisticated web platform that uses artificial intelligence to connect importers and exporters across all 54 AfCFTA member countries, with special focus on the 8 Guided Trade Initiative (GTI) priority markets.

## 🚀 Features

### Core Functionality
- **AI-Powered Matching**: Advanced machine learning algorithms analyze 16+ compatibility factors
- **AfCFTA Specialized**: Built specifically for African Continental Free Trade Area
- **GTI Priority Markets**: Special focus on Ghana, Kenya, Rwanda, Tanzania, Mauritius, Egypt, Cameroon, South Africa
- **Verified Network**: Comprehensive company profiles and business verification
- **Real-time Recommendations**: Dynamic matching based on user behavior and preferences

### Key Capabilities
- **Company Registration**: Separate flows for importers and exporters
- **Business Profiles**: Detailed company information, products/services, certifications
- **Smart Matching**: Compatibility scoring based on:
  - Geographic alignment (30% weight)
  - Product/service compatibility (40% weight)
  - Business size matching (15% weight)
  - Language compatibility (10% weight)
  - GTI priority boost (5% weight)
- **Trade Preferences**: Country preferences, trade volume, certifications
- **Dashboard Analytics**: User statistics, match insights, trade opportunities
- **AI Trade Assistant**: Intelligent chatbot for trade guidance and platform help
- **Trade Intelligence**: Real-time market analytics, trending products, country statistics
- **Finance Calculator**: Tools for calculating trade costs, duties, and profit margins
- **Document Management**: Upload, verify, and manage trade documents
- **Admin Panel**: Comprehensive user management, verification, and system monitoring

## 🛠 Technology Stack

- **Backend**: Python Flask with SQLAlchemy ORM
- **AI/ML**: scikit-learn for matching algorithms
- **Frontend**: Bootstrap 5 with vanilla JavaScript
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Gunicorn WSGI server

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+ installed
- pip package manager
- Git (optional)

### Quick Start

1. **Navigate to the project directory**:
   ```bash
   cd afcfta_matchmaker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create sample data** (optional but recommended for testing):
   ```bash
   python create_sample_data.py
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

### Sample Accounts (for testing)

After running `create_sample_data.py`, you can login with these credentials:

**Exporters:**
- `africagrains@example.com` / `password123` (Ghana - Agricultural Products)
- `eastexports@example.com` / `password123` (Kenya - Textiles)
- `pharmaexport@example.com` / `password123` (South Africa - Pharmaceuticals)
- `techexport@example.com` / `password123` (Rwanda - Technology)

**Importers:**
- `foodimport@example.com` / `password123` (Nigeria - Food Products)
- `fashionimport@example.com` / `password123` (Morocco - Fashion)
- `healthimport@example.com` / `password123` (Tanzania - Healthcare)
- `constructimport@example.com` / `password123` (Egypt - Construction)

**Administrator:**
- `admin@afcfta.com` / `admin123` (Full platform access)
- Access admin panel at: `http://localhost:5000/admin/login`

## 🌍 AfCFTA Coverage

### GTI Priority Countries (Active Trading)
- 🇬🇭 Ghana
- 🇰🇪 Kenya  
- 🇷🇼 Rwanda
- 🇹🇿 Tanzania
- 🇲🇺 Mauritius
- 🇪🇬 Egypt
- 🇨🇲 Cameroon
- 🇿🇦 South Africa

### All 54 AfCFTA Member Countries Supported
The platform covers all African Continental Free Trade Area member countries with specialized data and preferences.

## 🤖 AI Matching Algorithm

### Compatibility Factors
1. **Geographic Compatibility (30%)**
   - Different countries requirement
   - Preferred trading countries
   - Regional trade corridor optimization

2. **Product/Service Compatibility (40%)**
   - HS code category matching
   - Product intersection analysis
   - Service complementarity

3. **Business Size Compatibility (15%)**
   - Company size alignment
   - Trade volume matching
   - Operational capacity

4. **Language Compatibility (10%)**
   - Shared language identification
   - Communication efficiency

5. **GTI Priority Boost (5%)**
   - Active GTI country preference
   - AfCFTA implementation status

### Minimum Compatibility Threshold
- **30%** minimum score required for matches
- **Dynamic scoring** based on user interactions
- **Real-time updates** as profiles are completed

## 📊 Product Categories (HS Code Based)

- Agricultural Products & Food
- Textiles & Clothing
- Machinery & Equipment
- Electronics & Technology
- Chemicals & Pharmaceuticals
- Metals & Minerals
- Automotive & Transport Equipment
- Wood & Paper Products
- Plastics & Rubber
- Construction Materials
- Energy & Petroleum Products
- Handicrafts & Arts
- Services & Consulting

## 🔧 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### User Management
- `GET /profile` - View/edit user profile
- `POST /profile` - Update user profile

### Matching System
- `GET /dashboard` - Main dashboard with matches
- `POST /api/find-matches` - Get AI-powered matches (JSON)

### Enhanced Features
- `GET /trade-intelligence` - Trade analytics dashboard
- `GET /ai-chat` - AI Trade Assistant interface
- `POST /api/chat` - AI chat endpoint
- `GET /finance` - Finance calculator
- `GET /documents` - Document management
- `POST /api/upload-document` - Upload trade documents

### Admin Endpoints (Requires Admin Role)
- `POST /admin/login` - Admin authentication
- `GET /admin/dashboard` - Admin panel overview
- `GET /admin/users` - User management interface
- `POST /admin/verify-user/<id>` - Verify user account
- `POST /admin/toggle-user/<id>` - Activate/deactivate user
- `GET /admin/documents` - Document verification queue
- `POST /admin/verify-document/<id>` - Verify document
- `GET /admin/settings` - System configuration

## 🚀 Deployment

**READY FOR PRODUCTION DEPLOYMENT**

This application includes all configuration files needed for immediate deployment to popular hosting platforms.

### Quick Deploy Options

**Render (Recommended - Free Tier)**
- Includes `render.yaml` configuration
- One-click deployment from GitHub
- Automatic HTTPS and CDN

**Railway**
- Includes `railway.json` configuration
- Auto-deployment from Git push
- Free $5/month credit

**PythonAnywhere**
- Stable Flask hosting
- Free tier available
- Easy setup process

**Heroku**
- Includes `Procfile` configuration
- Classic platform
- Easy scaling

### Comprehensive Deployment Guide

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed step-by-step instructions for all platforms, including:
- Platform comparison
- Configuration steps
- Environment variable setup
- Database migration
- Post-deployment checklist
- Troubleshooting tips

### Production Setup (Manual)

1. **Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export DATABASE_URL=postgresql://user:pass@localhost/afcfta_db
   export SECRET_KEY=your-secret-key
   ```

2. **Database Migration**:
   ```bash
   # For PostgreSQL in production
   pip install psycopg2-binary
   # Database URL auto-configured via environment
   python app.py
   ```

3. **Gunicorn Deployment**:
   ```bash
   gunicorn --bind 0.0.0.0:8000 app:app
   ```

### Configuration Files Included

- `Procfile` - Process configuration for Heroku/Render
- `runtime.txt` - Python version specification
- `render.yaml` - Render platform configuration
- `railway.json` - Railway platform configuration
- `.slugignore` - Files to exclude from deployment

## 📈 Business Model & Market Opportunity

### Market Size
- **$81 billion** current intra-African trade (2023)
- **$450 billion** potential by 2035 with full AfCFTA implementation
- **45% increase** in intra-African exports expected by 2045

### Revenue Opportunities
1. **Freemium Model**: Basic matching free, premium features paid
2. **Subscription Tiers**: $99-$999/month based on features
3. **Transaction Fees**: Small percentage of successful trades
4. **API Licensing**: Sell matching technology to other platforms

### Competitive Advantages
- **First-mover** in AfCFTA-specific AI matching
- **Deep African market** understanding
- **GTI priority market** focus
- **Advanced AI algorithms** vs. basic directories

## 🔮 Roadmap

### Phase 1: MVP (Current)
- ✅ Core AI matching functionality
- ✅ User registration and profiles
- ✅ Basic dashboard and analytics
- ✅ AfCFTA country coverage
- ✅ Sample data and testing

### Phase 2: Enhanced Features (COMPLETED)
- ✅ AI Trade Assistant Chat
- ✅ Trade Intelligence Dashboard
- ✅ Finance Calculator
- ✅ Document Management System
- ✅ Comprehensive Admin Panel
- 🔄 Advanced messaging system
- 🔄 Mobile application
- 🔄 Payment integration
- 🔄 Trade financing connections

### Phase 3: Scale & Growth (6-12 months)
- 📋 API partnerships
- 📋 White-label solutions
- 📋 Advanced analytics
- 📋 Multi-language support
- 📋 Enterprise features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, email: support@afcfta-matchmaker.com

## 🙏 Acknowledgments

- African Union for AfCFTA initiative
- UN Economic Commission for Africa (UNECA)
- African Export-Import Bank (Afreximbank)
- All AfCFTA member countries

---

**Built with ❤️ for Africa's trade integration and economic growth.**

*Supporting the African Continental Free Trade Area vision of increased intra-African trade and economic development.*