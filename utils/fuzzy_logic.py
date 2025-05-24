import numpy as np

class FuzzyMamdani:
    def __init__(self):
        # Define membership function parameters
        self.rendah_params = {'start': 0, 'peak': 0, 'end': 20}
        self.sedang_params = {'start': 15, 'peak': 25, 'end': 35}
        self.tinggi_params = {'start': 30, 'peak': 50, 'end': 50}
        
        # Output crisp values for defuzzification
        self.output_values = {
            'aman': 20,
            'siaga': 50,
            'banjir': 80
        }
    
    def membership_rendah(self, x):
        """Membership function untuk tingkat air RENDAH (triangular left)"""
        if x <= 0:
            return 1.0
        elif 0 < x <= 20:
            return (20 - x) / (20 - 0)
        else:
            return 0.0
    
    def membership_sedang(self, x):
        """Membership function untuk tingkat air SEDANG (triangular)"""
        if x <= 15:
            return 0.0
        elif 15 < x <= 25:
            return (x - 15) / (25 - 15)
        elif 25 < x <= 35:
            return (35 - x) / (35 - 25)
        else:
            return 0.0
    
    def membership_tinggi(self, x):
        """Membership function untuk tingkat air TINGGI (triangular right)"""
        if x <= 30:
            return 0.0
        elif 30 < x <= 50:
            return (x - 30) / (50 - 30)
        else:
            return 1.0
    
    def fuzzifikasi(self, ketinggian):
        """Step 1: Fuzzifikasi - Hitung derajat keanggotaan"""
        mu_rendah = self.membership_rendah(ketinggian)
        mu_sedang = self.membership_sedang(ketinggian)
        mu_tinggi = self.membership_tinggi(ketinggian)
        
        return {
            'mu_rendah': round(mu_rendah, 3),
            'mu_sedang': round(mu_sedang, 3),
            'mu_tinggi': round(mu_tinggi, 3)
        }
    
    def inferensi(self, membership_values):
        """Step 2: Inferensi - Evaluasi aturan fuzzy"""
        rules = []
        
        # Rule 1: IF Rendah THEN Aman
        if membership_values['mu_rendah'] > 0:
            rules.append({
                'condition': 'Ketinggian = Rendah',
                'conclusion': 'Status = Aman',
                'strength': membership_values['mu_rendah'],
                'output': 'aman'
            })
        
        # Rule 2: IF Sedang THEN Siaga
        if membership_values['mu_sedang'] > 0:
            rules.append({
                'condition': 'Ketinggian = Sedang',
                'conclusion': 'Status = Siaga',
                'strength': membership_values['mu_sedang'],
                'output': 'siaga'
            })
        
        # Rule 3: IF Tinggi THEN Banjir
        if membership_values['mu_tinggi'] > 0:
            rules.append({
                'condition': 'Ketinggian = Tinggi',
                'conclusion': 'Status = Banjir',
                'strength': membership_values['mu_tinggi'],
                'output': 'banjir'
            })
        
        return rules
    
    def agregasi(self, active_rules):
        """Step 3: Agregasi - Gabungkan output dari semua aturan aktif"""
        aggregated = {}
        
        for rule in active_rules:
            output = rule['output']
            strength = rule['strength']
            
            if output not in aggregated:
                aggregated[output] = strength
            else:
                # Menggunakan MAX aggregation
                aggregated[output] = max(aggregated[output], strength)
        
        return aggregated
    
    def defuzzifikasi(self, aggregated_outputs):
        """Step 4: Defuzzifikasi menggunakan metode Centroid"""
        if not aggregated_outputs:
            return 0, "tidak_diketahui"
        
        # Hitung centroid
        numerator = 0
        denominator = 0
        
        for output_name, strength in aggregated_outputs.items():
            crisp_value = self.output_values[output_name]
            numerator += strength * crisp_value
            denominator += strength
        
        if denominator == 0:
            return 0, "tidak_diketahui"
        
        centroid_value = numerator / denominator
        
        # Tentukan status berdasarkan nilai centroid
        if centroid_value <= 30:
            status = "Aman"
        elif centroid_value <= 60:
            status = "Siaga"
        else:
            status = "Banjir"
        
        return round(centroid_value, 2), status
    
    def calculate_complete(self, ketinggian):
        """Perhitungan lengkap fuzzy Mamdani dengan detail step by step"""
        
        # Step 1: Fuzzifikasi
        membership = self.fuzzifikasi(ketinggian)
        
        # Step 2: Inferensi
        active_rules = self.inferensi(membership)
        
        # Step 3: Agregasi
        aggregated = self.agregasi(active_rules)
        
        # Step 4: Defuzzifikasi
        defuzz_value, final_status = self.defuzzifikasi(aggregated)
        
        return {
            'input': ketinggian,
            'step1_fuzzifikasi': membership,
            'step2_inferensi': active_rules,
            'step3_agregasi': aggregated,
            'step4_defuzzifikasi': {
                'centroid_value': defuzz_value,
                'final_status': final_status
            },
            'summary': {
                'ketinggian_air': ketinggian,
                'mu_rendah': membership['mu_rendah'],
                'mu_sedang': membership['mu_sedang'],
                'mu_tinggi': membership['mu_tinggi'],
                'defuzzifikasi_nilai': defuzz_value,
                'status': final_status
            }
        }
    
    def generate_membership_chart_data(self):
        """Generate data untuk grafik membership functions"""
        x = np.linspace(0, 50, 100)
        
        rendah_values = [self.membership_rendah(xi) for xi in x]
        sedang_values = [self.membership_sedang(xi) for xi in x]
        tinggi_values = [self.membership_tinggi(xi) for xi in x]
        
        return {
            'x': x.tolist(),
            'rendah': rendah_values,
            'sedang': sedang_values,
            'tinggi': tinggi_values
        }
