from flask import Blueprint, render_template, jsonify, session
from models import db
from models.monitoring import MonitoringData
from routes.auth import login_required
from datetime import datetime, timedelta
import json

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard utama dengan grafik dan statistik"""
    
    # Ambil data terbaru
    latest_data = MonitoringData.query.order_by(MonitoringData.timestamp.desc()).first()
    
    # Statistik hari ini
    today = datetime.now().date()
    today_data = MonitoringData.query.filter(
        db.func.date(MonitoringData.timestamp) == today
    ).all()
    
    # Hitung statistik status
    status_counts = {}
    for data in today_data:
        status = data.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Data untuk grafik 24 jam terakhir
    last_24h = datetime.now() - timedelta(hours=24)
    chart_data = MonitoringData.query.filter(
        MonitoringData.timestamp >= last_24h
    ).order_by(MonitoringData.timestamp.asc()).all()
    
    return render_template('dashboard.html', 
                         latest_data=latest_data,
                         status_counts=status_counts,
                         total_today=len(today_data),
                         chart_data=[data.to_dict() for data in chart_data])

@dashboard_bp.route('/monitoring')
@login_required
def monitoring():
    """Halaman monitoring data sensor real-time"""
    
    # Ambil 50 data terbaru
    monitoring_data = MonitoringData.query.order_by(
        MonitoringData.timestamp.desc()
    ).limit(50).all()
    
    return render_template('monitoring.html', 
                         monitoring_data=monitoring_data)

@dashboard_bp.route('/api/latest-data')
@login_required
def get_latest_data():
    """API untuk mendapatkan data terbaru (untuk real-time update)"""
    
    latest = MonitoringData.query.order_by(MonitoringData.timestamp.desc()).first()
    
    if latest:
        return jsonify({
            'success': True,
            'data': latest.to_dict()
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Tidak ada data'
        })

@dashboard_bp.route('/api/chart-data')
@login_required
def get_chart_data():
    """API untuk data grafik real-time"""
    
    # Data 2 jam terakhir
    last_2h = datetime.now() - timedelta(hours=2)
    data = MonitoringData.query.filter(
        MonitoringData.timestamp >= last_2h
    ).order_by(MonitoringData.timestamp.asc()).all()
    
    chart_data = []
    for item in data:
        chart_data.append({
            'timestamp': item.timestamp.strftime('%H:%M:%S'),
            'ketinggian': item.ketinggian_air,
            'status': item.status
        })
    
    return jsonify({
        'success': True,
        'data': chart_data
    })