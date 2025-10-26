import os
import sys
import json
import numpy as np
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, os.path.abspath('.'))

from app import app, db, User, TradeMatch, AdminSettings, AdminLog, Document, ChatMessage, TradeInsight, FinanceCalculation, AFCFTA_COUNTRIES, GTI_COUNTRIES, PRODUCT_CATEGORIES

def create_sample_data():
    """Create sample users and data for testing the platform"""
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print("Creating sample AfCFTA trade data...")
        
        # Create Admin User
        admin_user = User(
            email='admin@afcfta.com',
            company_name='AfCFTA Admin',
            user_type='admin',
            country='Multi-Country',
            contact_person='System Administrator',
            is_admin=True,
            is_verified=True,
            is_active=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        print("✅ Admin user created: admin@afcfta.com | Password: admin123")
        print("   This admin account has full access to the admin panel.")
        print()
        
        # Sample Exporters
        exporters = [
            {
                'email': 'africagrains@example.com',
                'company_name': 'Africa Grains Export Ltd',
                'country': 'Ghana',
                'user_type': 'exporter',
                'contact_person': 'Kwame Asante',
                'phone': '+233 XXX XXX XXX',
                'business_description': 'Leading exporter of premium cocoa, coffee, and cashew nuts from West Africa. We specialize in organic and fair-trade certified products with 20+ years of experience in international trade.',
                'products_services': json.dumps(['agricultural_products']),
                'annual_volume': '1m_5m',
                'company_size': 'medium',
                'certifications': 'Organic Certification, Fair Trade, HACCP, ISO 22000',
                'languages': 'English, French, Twi',
                'preferred_countries': json.dumps(['Kenya', 'South Africa', 'Nigeria', 'Egypt']),
                'website': 'https://africagrains.com'
            },
            {
                'email': 'eastexports@example.com',
                'company_name': 'East African Textiles Co.',
                'country': 'Kenya',
                'user_type': 'exporter',
                'contact_person': 'Amina Hassan',
                'phone': '+254 XXX XXX XXX',
                'business_description': 'Manufacturer and exporter of high-quality cotton textiles, traditional African fabrics, and modern apparel. We combine traditional craftsmanship with modern manufacturing techniques.',
                'products_services': json.dumps(['textiles_clothing']),
                'annual_volume': '500k_1m',
                'company_size': 'small',
                'certifications': 'OEKO-TEX Standard 100, GOTS (Global Organic Textile Standard)',
                'languages': 'English, Swahili, Arabic',
                'preferred_countries': json.dumps(['Ghana', 'South Africa', 'Rwanda', 'Tanzania']),
                'website': 'https://eastafricantextiles.co.ke'
            },
            {
                'email': 'pharmaexport@example.com',
                'company_name': 'African Pharmaceuticals Export',
                'country': 'South Africa',
                'user_type': 'exporter',
                'contact_person': 'Dr. Nelson Mandela Jr.',
                'phone': '+27 XXX XXX XXX',
                'business_description': 'Leading pharmaceutical exporter specializing in generic medicines, traditional African remedies, and medical equipment. WHO-approved manufacturing facilities with international quality standards.',
                'products_services': json.dumps(['chemicals_pharmaceuticals']),
                'annual_volume': '5m_plus',
                'company_size': 'large',
                'certifications': 'WHO GMP, FDA Approved, ISO 13485, ISO 14001',
                'languages': 'English, Afrikaans, Zulu, Xhosa',
                'preferred_countries': json.dumps(['Ghana', 'Kenya', 'Nigeria', 'Egypt', 'Morocco']),
                'website': 'https://africapharmaexport.co.za'
            },
            {
                'email': 'techexport@example.com',
                'company_name': 'Rwanda Tech Solutions',
                'country': 'Rwanda',
                'user_type': 'exporter',
                'contact_person': 'Jean Paul Kagame',
                'phone': '+250 XXX XXX XXX',
                'business_description': 'Innovative technology solutions provider exporting software, mobile applications, and IT consulting services across Africa. Specializing in fintech, agtech, and e-commerce solutions.',
                'products_services': json.dumps(['electronics_technology', 'services_consulting']),
                'annual_volume': '100k_500k',
                'company_size': 'small',
                'certifications': 'ISO 27001, CMMI Level 3, Microsoft Gold Partner',
                'languages': 'English, French, Kinyarwanda',
                'preferred_countries': json.dumps(['Kenya', 'Ghana', 'Tanzania', 'Uganda']),
                'website': 'https://rwandatech.rw'
            }
        ]
        
        # Sample Importers
        importers = [
            {
                'email': 'foodimport@example.com',
                'company_name': 'Continental Food Imports',
                'country': 'Nigeria',
                'user_type': 'importer',
                'contact_person': 'Chinwe Okafor',
                'phone': '+234 XXX XXX XXX',
                'business_description': 'Major food importer supplying supermarket chains and retail outlets across West Africa. We focus on high-quality agricultural products, processed foods, and beverages.',
                'products_services': json.dumps(['agricultural_products']),
                'annual_volume': '1m_5m',
                'company_size': 'medium',
                'certifications': 'NAFDAC Approved, HACCP, Halal Certification',
                'languages': 'English, Hausa, Igbo, Yoruba',
                'preferred_countries': json.dumps(['Ghana', 'Ivory Coast', 'Cameroon', 'Senegal']),
                'website': 'https://continentalfood.ng'
            },
            {
                'email': 'fashionimport@example.com',
                'company_name': 'African Fashion Hub',
                'country': 'Morocco',
                'user_type': 'importer',
                'contact_person': 'Fatima Al-Zahra',
                'phone': '+212 XXX XXX XXX',
                'business_description': 'Premium fashion retailer importing contemporary African designs, traditional textiles, and modern apparel. We operate 15 stores across North Africa and distribute to European markets.',
                'products_services': json.dumps(['textiles_clothing', 'handicrafts_arts']),
                'annual_volume': '500k_1m',
                'company_size': 'medium',
                'certifications': 'CE Marking, REACH Compliance',
                'languages': 'Arabic, French, English, Berber',
                'preferred_countries': json.dumps(['Kenya', 'Ghana', 'South Africa', 'Senegal']),
                'website': 'https://africanfashionhub.ma'
            },
            {
                'email': 'healthimport@example.com',
                'company_name': 'East Africa Health Supplies',
                'country': 'Tanzania',
                'user_type': 'importer',
                'contact_person': 'Dr. Mwalimu Nyerere',
                'phone': '+255 XXX XXX XXX',
                'business_description': 'Healthcare supply chain specialist importing medical equipment, pharmaceuticals, and healthcare technologies for hospitals and clinics across East Africa.',
                'products_services': json.dumps(['chemicals_pharmaceuticals', 'machinery_equipment']),
                'annual_volume': '1m_5m',
                'company_size': 'small',
                'certifications': 'TMDA Approved, ISO 13485, WHO Prequalification',
                'languages': 'English, Swahili, Arabic',
                'preferred_countries': json.dumps(['South Africa', 'Kenya', 'Egypt', 'Morocco']),
                'website': 'https://healthsupplies.tz'
            },
            {
                'email': 'constructimport@example.com',
                'company_name': 'Pyramid Construction Imports',
                'country': 'Egypt',
                'user_type': 'importer',
                'contact_person': 'Ahmed Hassan El-Masry',
                'phone': '+20 XXX XXX XXX',
                'business_description': 'Leading construction materials importer serving major infrastructure projects across North Africa. We specialize in heavy machinery, building materials, and engineering equipment.',
                'products_services': json.dumps(['construction_materials', 'machinery_equipment']),
                'annual_volume': '5m_plus',
                'company_size': 'large',
                'certifications': 'CE Marking, ISO 9001, OHSAS 18001',
                'languages': 'Arabic, English, French',
                'preferred_countries': json.dumps(['South Africa', 'Morocco', 'Ghana', 'Kenya']),
                'website': 'https://pyramidconstruction.eg'
            },
            {
                'email': 'agricimport@example.com',
                'company_name': 'Mauritius Agri Imports',
                'country': 'Mauritius',
                'user_type': 'importer',
                'contact_person': 'Raj Patel',
                'phone': '+230 XXX XXX XXX',
                'business_description': 'Agricultural technology and equipment importer serving the Indian Ocean islands and East Africa. We focus on sustainable farming solutions and modern agricultural machinery.',
                'products_services': json.dumps(['machinery_equipment', 'agricultural_products']),
                'annual_volume': '100k_500k',
                'company_size': 'micro',
                'certifications': 'ISO 9001, CE Marking',
                'languages': 'English, French, Hindi, Creole',
                'preferred_countries': json.dumps(['South Africa', 'Kenya', 'Tanzania', 'Madagascar']),
                'website': 'https://mauritiusagri.mu'
            }
        ]
        
        # Create all users
        all_users = exporters + importers
        created_users = []
        
        for user_data in all_users:
            user = User(
                email=user_data['email'],
                company_name=user_data['company_name'],
                user_type=user_data['user_type'],
                country=user_data['country'],
                contact_person=user_data['contact_person'],
                phone=user_data['phone'],
                business_description=user_data['business_description'],
                products_services=user_data['products_services'],
                annual_volume=user_data['annual_volume'],
                company_size=user_data['company_size'],
                certifications=user_data['certifications'],
                languages=user_data['languages'],
                preferred_countries=user_data['preferred_countries'],
                website=user_data['website']
            )
            user.set_password('password123')  # Default password for demo
            db.session.add(user)
            created_users.append(user)
        
        db.session.commit()
        
        print(f"Created {len(created_users)} sample users:")
        print("\nEXPORTERS:")
        for user in created_users:
            if user.user_type == 'exporter':
                products = json.loads(user.products_services or '[]')
                product_names = [PRODUCT_CATEGORIES.get(p, p) for p in products]
                print(f"  - {user.company_name} ({user.country}) - {', '.join(product_names)}")
        
        print("\nIMPORTERS:")
        for user in created_users:
            if user.user_type == 'importer':
                products = json.loads(user.products_services or '[]')
                product_names = [PRODUCT_CATEGORIES.get(p, p) for p in products]
                print(f"  - {user.company_name} ({user.country}) - {', '.join(product_names)}")
        
        print("\n" + "="*60)
        print("SAMPLE LOGIN CREDENTIALS (for testing):")
        print("🔐 ADMIN ACCESS:")
        print("Email: admin@afcfta.com | Password: admin123")
        print()
        print("👥 USER ACCOUNTS:")
        print("Email: africagrains@example.com | Password: password123")
        print("Email: foodimport@example.com | Password: password123")
        print("Email: eastexports@example.com | Password: password123")
        print("(All demo accounts use 'password123')")
        print("="*60)
        
        # Create initial admin settings
        initial_settings = [
            ('platform_name', 'AfCFTA Trade Matchmaker'),
            ('min_match_score', '0.3'),
            ('max_matches_per_user', '10'),
            ('require_verification', 'false'),
            ('enable_gti_priority', 'true'),
            ('maintenance_mode', 'false')
        ]
        
        for key, value in initial_settings:
            setting = AdminSettings(
                setting_key=key,
                setting_value=value,
                updated_by=admin_user.id
            )
            db.session.add(setting)
        
        # Create initial admin log
        initial_log = AdminLog(
            admin_id=admin_user.id,
            action='INITIALIZE_PLATFORM',
            details='Platform initialized with sample data and default settings'
        )
        db.session.add(initial_log)
        
        # Create sample Trade Insights (commodity prices and market data)
        sample_commodities = [
            {'name': 'Cocoa', 'price': 2450.50, 'change': 2.3, 'volume': 8500, 'trend': 'rising'},
            {'name': 'Coffee', 'price': 158.75, 'change': -1.2, 'volume': 6200, 'trend': 'falling'},
            {'name': 'Cotton', 'price': 1.25, 'change': 0.8, 'volume': 9800, 'trend': 'rising'},
            {'name': 'Cocoa Butter', 'price': 4120.25, 'change': 1.9, 'volume': 3200, 'trend': 'rising'},
            {'name': 'Gold', 'price': 1975.30, 'change': 0.5, 'volume': 1500, 'trend': 'stable'},
            {'name': 'Copper', 'price': 8920.15, 'change': -0.7, 'volume': 4800, 'trend': 'falling'},
            {'name': 'Crude Oil', 'price': 78.45, 'change': 1.1, 'volume': 12000, 'trend': 'rising'},
            {'name': 'Shea Butter', 'price': 2150.80, 'change': 3.2, 'volume': 2100, 'trend': 'rising'}
        ]
        
        for commodity in sample_commodities:
            insight = TradeInsight(
                commodity_name=commodity['name'],
                current_price=commodity['price'],
                price_change=commodity['change'],
                volume_traded=commodity['volume'],
                source_country=np.random.choice(GTI_COUNTRIES),
                destination_country=np.random.choice(GTI_COUNTRIES),
                market_trend=commodity['trend']
            )
            db.session.add(insight)
        
        # Create sample documents for demonstration
        sample_documents = [
            {
                'user': created_users[0],  # First exporter
                'type': 'certificate_of_origin',
                'name': 'Cocoa Export Certificate - Ghana 2025'
            },
            {
                'user': created_users[1],  # Second exporter
                'type': 'quality_certificate',
                'name': 'Organic Coffee Certification - Kenya'
            },
            {
                'user': created_users[2],  # Third exporter
                'type': 'business_certificate',
                'name': 'South Africa Export License'
            }
        ]
        
        for doc_data in sample_documents:
            doc = Document(
                user_id=doc_data['user'].id,
                document_type=doc_data['type'],
                document_name=doc_data['name'],
                verification_status='verified',
                verified_at=datetime.utcnow(),
                verified_by=admin_user.id
            )
            db.session.add(doc)
        
        # Create sample chat messages
        sample_chats = [
            {
                'user': created_users[0],
                'message': 'What are the current cocoa prices in West Africa?',
                'response': 'Current cocoa prices in West Africa are around $2,450/ton, showing a 2.3% increase. This is driven by strong demand for premium Ghanaian cocoa. Would you like specific pricing for a particular region or market?'
            },
            {
                'user': created_users[1],
                'message': 'How do I find coffee importers in Egypt?',
                'response': 'I can help you connect with coffee importers in Egypt! Our AI has identified several potential buyers in the Egyptian market. The GTI initiative also offers streamlined trade procedures between Kenya and Egypt for coffee exports.'
            }
        ]
        
        for chat_data in sample_chats:
            chat = ChatMessage(
                user_id=chat_data['user'].id,
                message=chat_data['message'],
                response=chat_data['response']
            )
            db.session.add(chat)
        
        # Create sample finance calculations
        sample_calculations = [
            {
                'user': created_users[0],
                'type': 'working_capital',
                'parameters': {'invoice_amount': 50000, 'payment_terms_days': 30, 'operating_cycle_days': 60},
                'result': {'working_capital_needed': 50000, 'lending_rate': 8.5, 'interest_cost': 347}
            },
            {
                'user': created_users[1],
                'type': 'letter_of_credit',
                'parameters': {'transaction_value': 100000},
                'result': {'lc_fee': 300, 'processing_time': '5-10 business days'}
            }
        ]
        
        for calc_data in sample_calculations:
            calc = FinanceCalculation(
                user_id=calc_data['user'].id,
                calculation_type=calc_data['type'],
                parameters=json.dumps(calc_data['parameters']),
                result=json.dumps(calc_data['result'])
            )
            db.session.add(calc)
        
        db.session.commit()
        
        return created_users

if __name__ == '__main__':
    create_sample_data()
    print("\nSample data created successfully!")
    print("\nTo run the application:")
    print("1. pip install -r requirements.txt")
    print("2. python app.py")
    print("3. Open http://localhost:5000")