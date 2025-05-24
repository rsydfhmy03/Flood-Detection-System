from datetime import datetime
from datetime import datetime
# from models import db  # ✅ benar karena db dideklarasikan di models/__init__.py
from extensions import db

from werkzeug.security import generate_password_hash, check_password_hash
class MonitoringData(db.Model):
    __tablename__ = 'monitoring_data'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ketinggian_air = db.Column(db.Float, nullable=False)
    jarak_sensor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    
    # Fuzzy Logic Values
    mu_rendah = db.Column(db.Float, default=0.0)
    mu_sedang = db.Column(db.Float, default=0.0)
    mu_tinggi = db.Column(db.Float, default=0.0)
    defuzzifikasi_nilai = db.Column(db.Float, default=0.0)
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ketinggian_air': self.ketinggian_air,
            'jarak_sensor': self.jarak_sensor,
            'status': self.status,
            'mu_rendah': self.mu_rendah,
            'mu_sedang': self.mu_sedang,
            'mu_tinggi': self.mu_tinggi,
            'defuzzifikasi_nilai': self.defuzzifikasi_nilai,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def __repr__(self):
        return f'<MonitoringData {self.id}: {self.ketinggian_air}cm - {self.status}>'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def __repr__(self):
        return f'<User {self.username}>'
