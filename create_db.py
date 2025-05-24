from app import app, db
from models.monitoring import MonitoringData, User
from werkzeug.security import generate_password_hash

def create_database():
    with app.app_context():
        # Drop all tables (hati-hati!)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create default admin user
        admin_user = User(
            username='admin',
            password=generate_password_hash('admin123'),  # Sesuaikan dengan field di model
            email='admin@example.com'
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("✅ Database created successfully!")
        print("👤 Default login: admin / admin123")

if __name__ == '__main__':
    create_database()