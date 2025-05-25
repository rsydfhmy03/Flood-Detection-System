# utils/pdf_generator.py
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF
from datetime import datetime, timedelta
import io
import os
from urllib.request import urlopen
from reportlab.lib.utils import ImageReader


class FloodMonitoringPDF:
    def __init__(self):
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom styles untuk PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            textColor=colors.HexColor('#1e40af'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=24
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            textColor=colors.HexColor('#3b82f6'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=13,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#1f2937'),
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#3b82f6'),
            borderPadding=8,
            backColor=colors.HexColor('#f8fafc'),
            alignment=TA_LEFT
        ))
        
        # Custom body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.HexColor('#374151'),
            alignment=TA_JUSTIFY
        ))

    def get_logo_from_url(self, url):
        """Download dan return logo dari URL"""
        try:
            response = urlopen(url)
            return ImageReader(io.BytesIO(response.read()))
        except Exception as e:
            print(f"Error downloading logo: {e}")
            return None

    def create_header_footer(self, canvas, doc):
        """Create header and footer untuk setiap halaman"""
        canvas.saveState()
        
        # Header background
        canvas.setFillColor(colors.HexColor('#1e40af'))
        canvas.rect(0, self.height - 80, self.width, 80, fill=True)
        
        # Logo
        logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Lambang_Kabupaten_Lumajang.png/657px-Lambang_Kabupaten_Lumajang.png"
        logo = self.get_logo_from_url(logo_url)
        if logo:
            try:
                canvas.drawImage(logo, 20, self.height - 75, width=60, height=70, mask='auto')
            except:
                pass  # Jika gagal load logo, lanjut tanpa logo
        
        # Header text
        canvas.setFillColor(colors.white)
        canvas.setFont('Helvetica-Bold', 14)
        canvas.drawString(95, self.height - 30, "SISTEM PERINGATAN DINI BANJIR")
        canvas.drawString(95, self.height - 45, "DESA ROWOKANGKUNG LUMAJANG")
        
        canvas.setFont('Helvetica', 9)
        canvas.drawString(95, self.height - 60, "Pemerintah Kabupaten Lumajang")
        
        # Timestamp di kanan atas
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(self.width - 20, self.height - 30, 
                              f"Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        # Footer
        canvas.setFillColor(colors.HexColor('#f3f4f6'))
        canvas.rect(0, 0, self.width, 35, fill=True)
        
        canvas.setFillColor(colors.HexColor('#6b7280'))
        canvas.setFont('Helvetica', 8)
        canvas.drawString(20, 15, "© 2025 Sistem Peringatan Dini Banjir Desa Rowokangkung - Kabupaten Lumajang by Mitahudev29")
        canvas.drawRightString(self.width - 20, 15, f"Halaman {doc.page}")
        
        canvas.restoreState()

    def create_summary_stats(self, data_list):
        """Buat ringkasan statistik"""
        if not data_list:
            return []
        
        # Hitung statistik
        total_records = len(data_list)
        status_counts = {}
        ketinggian_values = []
        
        for item in data_list:
            status = item.get('Status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
            
            try:
                ketinggian = float(item.get('Ketinggian', 0))
                ketinggian_values.append(ketinggian)
            except:
                pass
        
        avg_ketinggian = sum(ketinggian_values) / len(ketinggian_values) if ketinggian_values else 0
        max_ketinggian = max(ketinggian_values) if ketinggian_values else 0
        min_ketinggian = min(ketinggian_values) if ketinggian_values else 0
        
        # Buat tabel statistik
        stats_data = [
            ['Metrik', 'Nilai', 'Keterangan'],
            ['Total Record', str(total_records), 'Data monitoring terkumpul'],
            ['Ketinggian Rata-rata', f'{avg_ketinggian:.2f} cm', 'Rata-rata ketinggian air'],
            ['Ketinggian Maksimum', f'{max_ketinggian:.2f} cm', 'Ketinggian air tertinggi'],
            ['Ketinggian Minimum', f'{min_ketinggian:.2f} cm', 'Ketinggian air terendah'],
        ]
        
        # Tambahkan status counts
        for status, count in status_counts.items():
            percentage = (count / total_records) * 100
            stats_data.append([f'Status {status}', f'{count} ({percentage:.1f}%)', f'Jumlah record dengan status {status}'])
        
        stats_table = Table(stats_data, colWidths=[4*cm, 3*cm, 6.5*cm])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return [stats_table]

    def create_status_legend(self):
        """Buat legend untuk status"""
        legend_data = [
            ['Status', 'Indikator', 'Keterangan'],
            ['AMAN', '🟢', 'Ketinggian air normal, tidak ada risiko banjir'],
            ['WASPADA', '🟡', 'Ketinggian air mulai meningkat, perlu pemantauan'],
            ['BAHAYA', '🔴', 'Ketinggian air tinggi, potensi banjir tinggi'],
        ]
        
        legend_table = Table(legend_data, colWidths=[3*cm, 2*cm, 8.5*cm])
        legend_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fffbeb')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#f59e0b')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return legend_table

    def create_monitoring_table(self, data_list, page_size=28):
        """Buat tabel data monitoring dengan pagination yang lebih efisien"""
        if not data_list:
            return [Paragraph("Tidak ada data monitoring tersedia.", self.styles['CustomBody'])]
        
        tables = []
        
        # Bagi data menjadi chunks per halaman (lebih banyak per halaman)
        for i in range(0, len(data_list), page_size):
            chunk = data_list[i:i + page_size]
            
            # Header tabel dengan kolom yang lebih lebar
            table_data = [
                ['No', 'Waktu', 'Ketinggian\n(cm)', 'Jarak\n(cm)', 'Status', 
                 'μ Rendah', 'μ Sedang', 'μ Tinggi', 'Defuzzifikasi']
            ]
            
            # Data rows
            for idx, item in enumerate(chunk, start=i+1):
                # Format timestamp
                timestamp = item.get('Timestamp', 'N/A')
                if isinstance(timestamp, str) and len(timestamp) > 16:
                    timestamp = timestamp[:16]  # Potong untuk menghemat ruang
                
                # Status dengan warna
                status = item.get('Status', 'N/A')
                
                row = [
                    str(idx),
                    timestamp,
                    f"{item.get('Ketinggian', 'N/A')}",
                    f"{item.get('Jarak', 'N/A')}",
                    status,
                    f"{float(item.get('μ Rendah', 0)):.3f}" if item.get('μ Rendah') else 'N/A',
                    f"{float(item.get('μ Sedang', 0)):.3f}" if item.get('μ Sedang') else 'N/A',
                    f"{float(item.get('μ Tinggi', 0)):.3f}" if item.get('μ Tinggi') else 'N/A',
                    f"{float(item.get('Defuzzifikasi', 0)):.2f}" if item.get('Defuzzifikasi') else 'N/A',
                ]
                table_data.append(row)
            
            # Buat tabel dengan kolom width yang diperbaiki
            table = Table(table_data, colWidths=[
                0.8*cm,   # No
                2.8*cm,   # Waktu
                1.8*cm,   # Ketinggian  
                1.6*cm,   # Jarak
                2.0*cm,   # Status
                1.5*cm,   # μ Rendah
                1.5*cm,   # μ Sedang
                1.5*cm,   # μ Tinggi
                2.0*cm    # Defuzzifikasi (diperlebar)
            ])
            
            # Style tabel
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ]
            
            # Warna berdasarkan status
            for row_idx, item in enumerate(chunk, start=1):
                status = item.get('Status', '').upper()
                if status == 'BAHAYA':
                    table_style.append(('BACKGROUND', (4, row_idx), (4, row_idx), colors.HexColor('#fee2e2')))
                    table_style.append(('TEXTCOLOR', (4, row_idx), (4, row_idx), colors.HexColor('#dc2626')))
                    table_style.append(('FONTNAME', (4, row_idx), (4, row_idx), 'Helvetica-Bold'))
                elif status == 'WASPADA':
                    table_style.append(('BACKGROUND', (4, row_idx), (4, row_idx), colors.HexColor('#fef3c7')))
                    table_style.append(('TEXTCOLOR', (4, row_idx), (4, row_idx), colors.HexColor('#d97706')))
                    table_style.append(('FONTNAME', (4, row_idx), (4, row_idx), 'Helvetica-Bold'))
                elif status == 'AMAN':
                    table_style.append(('BACKGROUND', (4, row_idx), (4, row_idx), colors.HexColor('#dcfce7')))
                    table_style.append(('TEXTCOLOR', (4, row_idx), (4, row_idx), colors.HexColor('#16a34a')))
                    table_style.append(('FONTNAME', (4, row_idx), (4, row_idx), 'Helvetica-Bold'))
            
            table.setStyle(TableStyle(table_style))
            tables.append(table)
            
            # Tambah page break kecuali untuk tabel terakhir
            if i + page_size < len(data_list):
                tables.append(PageBreak())
        
        return tables

    def generate_pdf(self, data_list, filename="monitoring_report.pdf"):
        """Generate PDF lengkap"""
        buffer = io.BytesIO()
        
        # Setup document dengan margin yang disesuaikan untuk header/footer
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=2.5*cm,  # Diperbesar untuk header
            bottomMargin=1.5*cm
        )
        
        # Content list
        story = []
        
        # Title dan info
        story.append(Paragraph("LAPORAN MONITORING SISTEM PERINGATAN DINI BANJIR", self.styles['CustomTitle']))
        story.append(Paragraph("DESA ROWOKANGKUNG - KABUPATEN LUMAJANG", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Info laporan
        report_info = f"""
        <b>Periode Laporan:</b> {datetime.now().strftime('%d %B %Y')}<br/>
        <b>Total Data:</b> {len(data_list)} record monitoring<br/>
        <b>Sistem:</b> Monitoring Ketinggian Air Berbasis Sensor Ultrasonik<br/>
        <b>Metode Analisis:</b> Fuzzy Logic untuk Klasifikasi Status Peringatan Banjir<br/>
        <b>Lokasi:</b> Desa Rowokangkung, Kecamatan Rowokangkung, Kabupaten Lumajang
        """
        story.append(Paragraph(report_info, self.styles['CustomBody']))
        story.append(Spacer(1, 0.4*inch))
        
        # Ringkasan Statistik
        story.append(Paragraph("RINGKASAN STATISTIK MONITORING", self.styles['SectionHeader']))
        stats_elements = self.create_summary_stats(data_list)
        story.extend(stats_elements)
        story.append(Spacer(1, 0.3*inch))
        
        # Legend Status
        story.append(Paragraph("KETERANGAN STATUS PERINGATAN", self.styles['SectionHeader']))
        story.append(self.create_status_legend())
        story.append(Spacer(1, 0.4*inch))
        
        # Data Monitoring
        story.append(Paragraph("DATA MONITORING DETAIL", self.styles['SectionHeader']))
        story.append(Paragraph(
            "Berikut adalah data detail hasil monitoring sensor dengan nilai membership function "
            "untuk setiap kategori (Rendah, Sedang, Tinggi) dan hasil defuzzifikasi untuk "
            "menentukan status peringatan banjir:",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.2*inch))
        
        # Tabel monitoring
        monitoring_tables = self.create_monitoring_table(data_list)
        story.extend(monitoring_tables)
        
        # Footer info
        story.append(Spacer(1, 0.4*inch))
        footer_text = """
        <b>Keterangan Teknis:</b><br/>
        • μ (mu) adalah nilai membership function dalam sistem logika fuzzy (0.000 - 1.000)<br/>
        • Defuzzifikasi adalah proses konversi nilai fuzzy menjadi nilai numerik untuk pengambilan keputusan<br/>
        • Status peringatan ditentukan berdasarkan aturan fuzzy yang telah dikalibrasi untuk kondisi lokal<br/>
        • Laporan ini dihasilkan secara otomatis oleh Sistem Peringatan Dini Banjir Desa Rowokangkung<br/>
        • Untuk informasi lebih lanjut hubungi: Pemerintah Desa Rowokangkung, Kabupaten Lumajang
        """
        story.append(Paragraph(footer_text, self.styles['CustomBody']))
        
        # Build PDF dengan header/footer
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        
        buffer.seek(0)
        return buffer

# Fungsi helper untuk integrasi dengan Flask
def generate_monitoring_pdf(data_list):
    """Generate PDF dan return buffer"""
    pdf_generator = FloodMonitoringPDF()
    return pdf_generator.generate_pdf(data_list)