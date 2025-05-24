from flask import Blueprint, request, jsonify
from models import db
from models.monitoring import MonitoringData
from utils.fuzzy_logic import FuzzyMamdani
from datetime import datetime
import json

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/monitoring/store', methods=['POST'])
def store_monitoring_data():
    """API endpoint untuk menerima data dari ESP32"""
    
    try:
        # Ambil data dari request
        if request.is_json:
            data = request.get_json()
        else:
            # Untuk form data dari ESP32
            data = {
                'ketinggian_air': float(request.form.get('ketinggian_air', 0)),
                'jarak_sensor': float(request.form.get('jarak_sensor', 0))
            }
        
        ketinggian = data.get('ketinggian_air', 0)
        jarak = data.get('jarak_sensor', 0)
        
        # Hitung fuzzy logic
        fuzzy = FuzzyMamdani()
        fuzzy_result = fuzzy.calculate_complete(ketinggian)
        
        # Simpan ke database
        monitoring_record = MonitoringData(
            ketinggian_air=ketinggian,
            jarak_sensor=jarak,
            status=fuzzy_result['summary']['status'],
            mu_rendah=fuzzy_result['summary']['mu_rendah'],
            mu_sedang=fuzzy_result['summary']['mu_sedang'],
            mu_tinggi=fuzzy_result['summary']['mu_tinggi'],
            defuzzifikasi_nilai=fuzzy_result['summary']['defuzzifikasi_nilai'],
            timestamp=datetime.now()
        )
        
        db.session.add(monitoring_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Data berhasil disimpan',
            'data': {
                'id': monitoring_record.id,
                'ketinggian_air': ketinggian,
                'status': fuzzy_result['summary']['status'],
                'defuzzifikasi': fuzzy_result['summary']['defuzzifikasi_nilai'],
                'timestamp': monitoring_record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            },
            'fuzzy_calculation': fuzzy_result
        }), 200
        
    except Exception as e:
        print(f"Error storing data: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 400

@api_bp.route('/monitoring/data', methods=['GET'])
def get_monitoring_data():
    """API untuk mendapatkan data monitoring (dengan pagination)"""
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        data = MonitoringData.query.order_by(
            MonitoringData.timestamp.desc()
        ).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in data.items],
            'pagination': {
                'page': page,
                'pages': data.pages,
                'per_page': per_page,
                'total': data.total
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 400
