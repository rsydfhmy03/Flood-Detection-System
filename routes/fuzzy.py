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
    
    # Generate data untuk grafik membership functions (kedua parameter)
    chart_data = fuzzy.generate_membership_chart_data()
    
    return render_template('fuzzy_manual.html', 
                         chart_data=json.dumps(chart_data))

@fuzzy_bp.route('/calculate', methods=['POST'])
@login_required
def calculate_fuzzy():
    """API untuk perhitungan fuzzy manual dengan 2 parameter"""
    
    try:
        data = request.get_json()
        ketinggian = float(data.get('ketinggian', 0))
        curah_hujan = float(data.get('curah_hujan', 0))
        
        # Validasi input ketinggian air
        if ketinggian < 0 or ketinggian > 100:
            return jsonify({
                'success': False,
                'message': 'Ketinggian air harus antara 0-100 cm'
            }), 400
        
        # Validasi input curah hujan
        if curah_hujan < 0 or curah_hujan > 300:
            return jsonify({
                'success': False,
                'message': 'Curah hujan harus antara 0-300 mm'
            }), 400
        
        fuzzy = FuzzyMamdani()
        result = fuzzy.calculate_complete(ketinggian, curah_hujan)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': 'Input harus berupa angka yang valid'
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 400

@fuzzy_bp.route('/membership-data')
@login_required
def get_membership_data():
    """API untuk mendapatkan data membership functions kedua parameter"""
    
    try:
        fuzzy = FuzzyMamdani()
        chart_data = fuzzy.generate_membership_chart_data()
        
        return jsonify({
            'success': True,
            'data': chart_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 400

@fuzzy_bp.route('/test-calculation')
@login_required
def test_calculation():
    """API untuk testing perhitungan dengan contoh data"""
    
    try:
        # Contoh data untuk testing
        test_cases = [
            {'ketinggian': 16, 'curah_hujan': 50},   # Expected: Aman
            {'ketinggian': 25, 'curah_hujan': 120},  # Expected: Siaga
            {'ketinggian': 35, 'curah_hujan': 150},  # Expected: Banjir
        ]
        
        fuzzy = FuzzyMamdani()
        results = []
        
        for case in test_cases:
            result = fuzzy.calculate_complete(case['ketinggian'], case['curah_hujan'])
            results.append({
                'input': case,
                'output': {
                    'status': result['step4_defuzzifikasi']['final_status'],
                    'centroid': result['step4_defuzzifikasi']['centroid_value']
                }
            })
        
        return jsonify({
            'success': True,
            'test_results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 400