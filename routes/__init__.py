from flask import Blueprint

def init_routes(app):
    from routes import auth, dashboard, api, fuzzy
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(fuzzy.bp)
