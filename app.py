# app.py
from flask import Flask
from config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        from models.monitoring import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Register Blueprints
        from routes.auth import auth_bp
        from routes.dashboard import dashboard_bp
        from routes.api import api_bp
        from routes.fuzzy import fuzzy_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(api_bp, url_prefix='/api')
        app.register_blueprint(fuzzy_bp)

        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
