import numpy as np

class FuzzyMamdani:
    def __init__(self):
        # Water level membership parameters
        self.water_params = {
            'rendah': {'start': 0, 'peak': 0, 'end': 20},
            'sedang': {'start': 15, 'peak': 25, 'end': 35},
            'tinggi': {'start': 30, 'peak': 50, 'end': 50}
        }
        
        # Rainfall membership parameters
        self.rain_params = {
            'rendah': {'start': 0, 'end': 100},
            'sedang': {'start': 50, 'peak': 100, 'end': 150},
            'tinggi': {'start': 100, 'end': 200}
        }
        
        # Output crisp values
        self.output_values = {
            'aman': 20,
            'siaga': 50,
            'banjir': 80
        }
        
        # Thresholds for final status
        self.status_thresholds = {
            'aman': 30,
            'siaga': 60,
            'banjir': 100
        }

    # Water level membership functions
    def membership_rendah_air(self, x):
        if x <= 0: return 1.0
        elif 0 < x <= 20: return (20 - x)/20
        else: return 0.0
    
    def membership_sedang_air(self, x):
        if x <= 15: return 0.0
        elif 15 < x <= 25: return (x - 15)/10
        elif 25 < x <= 35: return (35 - x)/10
        else: return 0.0
    
    def membership_tinggi_air(self, x):
        if x <= 30: return 0.0
        elif 30 < x <= 50: return (x - 30)/20
        else: return 1.0

    # Rainfall membership functions
    def membership_rendah_hujan(self, x):
        if x <= 0: return 1.0
        elif 0 < x <= 100: return (100 - x)/100
        else: return 0.0
    
    def membership_sedang_hujan(self, x):
        if x <= 50: return 0.0
        elif 50 < x <= 100: return (x - 50)/50
        elif 100 < x <= 150: return (150 - x)/50
        else: return 0.0
    
    def membership_tinggi_hujan(self, x):
        if x <= 100: return 0.0
        elif 100 < x <= 200: return (x - 100)/100
        else: return 1.0

    def fuzzifikasi(self, ketinggian, curah_hujan):
        """Fuzzification for both inputs"""
        return {
            'air': {
                'rendah': round(self.membership_rendah_air(ketinggian), 3),
                'sedang': round(self.membership_sedang_air(ketinggian), 3),
                'tinggi': round(self.membership_tinggi_air(ketinggian), 3)
            },
            'hujan': {
                'rendah': round(self.membership_rendah_hujan(curah_hujan), 3),
                'sedang': round(self.membership_sedang_hujan(curah_hujan), 3),
                'tinggi': round(self.membership_tinggi_hujan(curah_hujan), 3)
            }
        }

    def inferensi(self, membership_values):
        """Rule evaluation with AND (min) operator"""
        rules = []
        a = membership_values['air']
        h = membership_values['hujan']
        
        # Rule 1: IF Air=Rendah AND Hujan=Rendah THEN Aman
        strength = min(a['rendah'], h['rendah'])
        if strength > 0:
            rules.append({
                'condition': 'Air=Rendah AND Hujan=Rendah',
                'conclusion': 'Status=Aman',
                'strength': strength,
                'output': 'aman'
            })
        
        # Rule 2: IF Air=Rendah AND Hujan=Sedang THEN Aman
        strength = min(a['rendah'], h['sedang'])
        if strength > 0:
            rules.append({
                'condition': 'Air=Rendah AND Hujan=Sedang',
                'conclusion': 'Status=Aman',
                'strength': strength,
                'output': 'aman'
            })
            
        # Rule 3: IF Air=Rendah AND Hujan=Tinggi THEN Siaga
        strength = min(a['rendah'], h['tinggi'])
        if strength > 0:
            rules.append({
                'condition': 'Air=Rendah AND Hujan=Tinggi',
                'conclusion': 'Status=Siaga',
                'strength': strength,
                'output': 'siaga'
            })
            
        # Rule 4: IF Air=Sedang AND Hujan=Rendah THEN Siaga
        strength = min(a['sedang'], h['rendah'])
        if strength > 0:
            rules.append({
                'condition': 'Air=Sedang AND Hujan=Rendah',
                'conclusion': 'Status=Siaga',
                'strength': strength,
                'output': 'siaga'
            })
            
        # Rule 5: IF Air=Sedang AND Hujan=Sedang THEN Siaga
        strength = min(a['sedang'], h['sedang'])
        if strength > 0:
            rules.append({
                'condition': 'Air=Sedang AND Hujan=Sedang',
                'conclusion': 'Status=Siaga',
                'strength': strength,
                'output': 'siaga'
            })
            
        # Rule 6: IF Air=Sedang AND Hujan=Tinggi THEN Banjir
        strength = min(a['sedang'], h['tinggi'])
        if strength > 0:
            rules.append({
                'condition': 'Air=Sedang AND Hujan=Tinggi',
                'conclusion': 'Status=Banjir',
                'strength': strength,
                'output': 'banjir'
            })
            
        # Rule 7: IF Air=Tinggi AND Hujan=Rendah THEN Banjir
        strength = min(a['tinggi'], h['rendah'])
        if strength > 0:
            rules.append({
                'condition': 'Air=Tinggi AND Hujan=Rendah',
                'conclusion': 'Status=Banjir',
                'strength': strength,
                'output': 'banjir'
            })
            
        # Rule 8: IF Air=Tinggi AND Hujan=Sedang THEN Banjir
        strength = min(a['tinggi'], h['sedang'])
        if strength > 0:
            rules.append({
                'condition': 'Air=Tinggi AND Hujan=Sedang',
                'conclusion': 'Status=Banjir',
                'strength': strength,
                'output': 'banjir'
            })
            
        # Rule 9: IF Air=Tinggi AND Hujan=Tinggi THEN Banjir
        strength = min(a['tinggi'], h['tinggi'])
        if strength > 0:
            rules.append({
                'condition': 'Air=Tinggi AND Hujan=Tinggi',
                'conclusion': 'Status=Banjir',
                'strength': strength,
                'output': 'banjir'
            })
        
        return rules

    def agregasi(self, active_rules):
        """Combine outputs using max operator"""
        aggregated = {}
        for rule in active_rules:
            output = rule['output']
            strength = rule['strength']
            if output not in aggregated or strength > aggregated[output]:
                aggregated[output] = strength
        return aggregated

    def defuzzifikasi(self, aggregated_outputs):
        """Centroid defuzzification"""
        if not aggregated_outputs:
            return 0, "tidak_diketahui"
        
        numerator = sum(strength * self.output_values[output] 
                     for output, strength in aggregated_outputs.items())
        denominator = sum(aggregated_outputs.values())
        
        if denominator == 0:
            return 0, "tidak_diketahui"
            
        centroid = numerator / denominator
        
        # Determine final status
        if centroid <= self.status_thresholds['aman']:
            status = "Aman"
        elif centroid <= self.status_thresholds['siaga']:
            status = "Siaga"
        else:
            status = "Banjir"
            
        return round(centroid, 2), status

    def calculate_complete(self, ketinggian, curah_hujan):
        """Complete fuzzy calculation with both inputs"""
        fuzzified = self.fuzzifikasi(ketinggian, curah_hujan)
        rules = self.inferensi(fuzzified)
        aggregated = self.agregasi(rules)
        centroid, status = self.defuzzifikasi(aggregated)
        
        return {
            'input': {
                'ketinggian_air': ketinggian,
                'curah_hujan': curah_hujan
            },
            'step1_fuzzifikasi': fuzzified,
            'step2_inferensi': rules,
            'step3_agregasi': aggregated,
            'step4_defuzzifikasi': {
                'centroid_value': centroid,
                'final_status': status
            },
            'summary': {
                'defuzzifikasi_nilai': centroid,
                'status': status
            }
        }

    def generate_membership_chart_data(self):
        """Generate chart data for both inputs"""
        x_air = np.linspace(0, 50, 100)
        x_hujan = np.linspace(0, 200, 100)
        
        return {
            'air': {
                'x': x_air.tolist(),
                'rendah': [self.membership_rendah_air(xi) for xi in x_air],
                'sedang': [self.membership_sedang_air(xi) for xi in x_air],
                'tinggi': [self.membership_tinggi_air(xi) for xi in x_air]
            },
            'hujan': {
                'x': x_hujan.tolist(),
                'rendah': [self.membership_rendah_hujan(xi) for xi in x_hujan],
                'sedang': [self.membership_sedang_hujan(xi) for xi in x_hujan],
                'tinggi': [self.membership_tinggi_hujan(xi) for xi in x_hujan]
            }
        }