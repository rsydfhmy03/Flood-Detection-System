from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.monitoring import User
from werkzeug.security import check_password_hash
from extensions import db  # Import dari extensions.py, bukan dari app.py

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout berhasil!', 'success')
    return redirect(url_for('auth.login'))

def login_required(f):
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function