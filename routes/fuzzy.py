from flask import Blueprint, render_template, request, jsonify
from routes.auth import login_required
from utils.fuzzy_logic import FuzzyMamdani
import json

fuzzy_bp = Blueprint('fuzzy', __name__, url_prefix='/fuzzy')

@fuzzy_bp.route('/manual')
@login_required
def manual_calculation():
    """Halaman perhitungan manual fuzzy logic"""
    
    fuzzy = FuzzyMamdani()
    
    # Generate data untuk grafik membership functions
    chart_data = fuzzy.generate_membership_chart_data()
    
    return render_template('fuzzy_manual.html', 
                         chart_data=json.dumps(chart_data))

@fuzzy_bp.route('/calculate', methods=['POST'])
@login_required
def calculate_fuzzy():
    """API untuk perhitungan fuzzy manual"""
    
    try:
        data = request.get_json()
        ketinggian = float(data.get('ketinggian', 0))
        
        if ketinggian < 0 or ketinggian > 100:
            return jsonify({
                'success': False,
                'message': 'Ketinggian air harus antara 0-100 cm'
            }), 400
        
        fuzzy = FuzzyMamdani()
        result = fuzzy.calculate_complete(ketinggian)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 400

@fuzzy_bp.route('/membership-data')
@login_required
def get_membership_data():
    """API untuk mendapatkan data membership functions"""
    
    fuzzy = FuzzyMamdani()
    chart_data = fuzzy.generate_membership_chart_data()
    
    return jsonify({
        'success': True,
        'data': chart_data
    })
