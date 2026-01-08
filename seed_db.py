from app import app
from models import db, User, Supplier, Product, Project
from werkzeug.security import generate_password_hash

def seed_database():
    with app.app_context():
        db.create_all()
        print("Cleaning old data...")
        Project.query.delete()
        Product.query.delete()
        Supplier.query.delete()
        User.query.delete()
        
        admin = User(
            username='bussiness_owner',
            email='admin@example.com',
            password=generate_password_hash('123456', method='pbkdf2:sha256'),
            role='student'
        )
        db.session.add(admin)
        print("-> Added User: admin@example.com (Student)")

        # 1.5 Supplier User
        supplier_user = User(
            username='global_supplier',
            email='supplier@example.com',
            password=generate_password_hash('123456', method='pbkdf2:sha256'),
            role='supplier'
        )
        db.session.add(supplier_user)
        print("-> Added User: supplier@example.com (Supplier)")

        # 2. Rich Supplier Data
        suppliers_data = [
            # --- Fitness & Gym ---
            {'name': 'Amman Fitness Equipment Co.', 'location': 'Local (Jordan)', 'rating': 4.9, 'quality': 'High', 'shipping': 50.0, 'tax': 16.0, 'category': 'Gym'},
            {'name': 'Guangzhou PowerGym Factory', 'location': 'Global (China)', 'rating': 4.5, 'quality': 'Medium', 'shipping': 1200.0, 'tax': 5.0, 'category': 'Gym'},
            {'name': 'TechnoSport Italy', 'location': 'Global (Italy)', 'rating': 4.95, 'quality': 'Premium', 'shipping': 850.0, 'tax': 20.0, 'category': 'Gym'},
            {'name': 'US Gold-Standard Gyms', 'location': 'Global (USA)', 'rating': 4.8, 'quality': 'High', 'shipping': 1500.0, 'tax': 15.0, 'category': 'Gym'},
            
            # --- Cafe & Restaurant ---
            {'name': 'Arabica Coffee Roasters', 'location': 'Local (Jordan)', 'rating': 4.8, 'quality': 'High', 'shipping': 20.0, 'tax': 16.0, 'category': 'Cafe'},
            {'name': 'Espresso Machines Milan', 'location': 'Global (Italy)', 'rating': 4.9, 'quality': 'Premium', 'shipping': 400.0, 'tax': 18.0, 'category': 'Cafe'},
            {'name': 'China Tableware Bulk', 'location': 'Global (China)', 'rating': 4.2, 'quality': 'Low', 'shipping': 600.0, 'tax': 5.0, 'category': 'Cafe'},

            # --- Fashion & Clothing ---
            {'name': 'Zarqa Tex Fabrics', 'location': 'Local (Jordan)', 'rating': 4.3, 'quality': 'Medium', 'shipping': 25.0, 'tax': 16.0, 'category': 'Fashion'},
            {'name': 'Istanbul Fashion Wholesalers', 'location': 'Global (Turkey)', 'rating': 4.7, 'quality': 'High', 'shipping': 350.0, 'tax': 12.0, 'category': 'Fashion'},
            {'name': 'Vietnam Apparel Source', 'location': 'Global (Vietnam)', 'rating': 4.4, 'quality': 'Medium', 'shipping': 900.0, 'tax': 8.0, 'category': 'Fashion'},
            {'name': 'Premium Paris Garments', 'location': 'Global (France)', 'rating': 4.9, 'quality': 'Premium', 'shipping': 500.0, 'tax': 25.0, 'category': 'Fashion'},

            # --- Tech & Electronics ---
            {'name': 'Shenzhen Tech Hub', 'location': 'Global (China)', 'rating': 4.6, 'quality': 'Variable', 'shipping': 500.0, 'tax': 5.0, 'category': 'Tech'},
            {'name': 'Amman PC Distributors', 'location': 'Local (Jordan)', 'rating': 4.5, 'quality': 'High', 'shipping': 30.0, 'tax': 16.0, 'category': 'Tech'},
            {'name': 'Silicon Valley Imports', 'location': 'Global (USA)', 'rating': 5.0, 'quality': 'Premium', 'shipping': 150.0, 'tax': 25.0, 'category': 'Tech'},
        ]

        supplier_objects = []
        for s in suppliers_data:
            supplier = Supplier(
                name=s['name'],
                location=s['location'],
                contact_info=f"contact@{s['name'].lower().replace(' ', '')}.com",
                product_quality=s['quality'],
                rating=s['rating'],
                shipping_cost=s['shipping'],
                taxes=s['tax']
            )
            db.session.add(supplier)
            supplier_objects.append((supplier, s['category']))
        
        db.session.commit()
        print(f"-> Added {len(suppliers_data)} suppliers.")

        # 3. Add Products for Smart Search
        products = []
        for supplier, category in supplier_objects:
            if category == 'Gym':
                products.extend([
                    Product(name='Treadmill Commercial', category='Gym', base_price=1200, supplier_id=supplier.id),
                    Product(name='Dumbbell Set 5-50kg', category='Gym', base_price=500, supplier_id=supplier.id),
                    Product(name='Multi-Gym Station', category='Gym', base_price=3500, supplier_id=supplier.id),
                    Product(name='Bench Press Rack', category='Gym', base_price=450, supplier_id=supplier.id),
                    Product(name='Olympic Barbell', category='Gym', base_price=200, supplier_id=supplier.id)
                ])
            elif category == 'Cafe':
                products.extend([
                    Product(name='Espresso Machine 2 Group', category='Cafe', base_price=2500, supplier_id=supplier.id),
                    Product(name='Coffee Beans Wholesale', category='Cafe', base_price=15, supplier_id=supplier.id),
                    Product(name='Industrial Grinder', category='Cafe', base_price=800, supplier_id=supplier.id)
                ])
            elif category == 'Fashion':
                products.extend([
                    Product(name='Cotton T-Shirts Bulk', category='Clothing', base_price=5, supplier_id=supplier.id),
                    Product(name='Denim Jeans Wholesale', category='Clothing', base_price=12, supplier_id=supplier.id),
                    Product(name='Hoodies High Quality', category='Clothing', base_price=18, supplier_id=supplier.id),
                    Product(name='Formal Suits', category='Clothing', base_price=85, supplier_id=supplier.id)
                ])
            elif category == 'Tech':
                products.extend([
                    Product(name='Gaming PC Components', category='Electronics', base_price=800, supplier_id=supplier.id),
                    Product(name='Smart Home Sensors', category='Electronics', base_price=40, supplier_id=supplier.id)
                ])

        db.session.add_all(products)
        db.session.commit()
        print(f"-> Added {len(products)} products.")
        print("Database initialized successfully.")

if __name__ == '__main__':
    seed_database()
