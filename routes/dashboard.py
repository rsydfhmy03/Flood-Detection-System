from flask import Blueprint, render_template, jsonify, session
from models import db
from models.monitoring import MonitoringData
from routes.auth import login_required
from datetime import datetime, timedelta
import json
from utils.pdf_generator import generate_monitoring_pdf

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
    from flask import request, Response, send_file
    import io, csv
    import pandas as pd
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    status_filter = request.args.get('status')
    export = request.args.get('export')  # csv, excel, pdf
    limit = request.args.get('limit', '50')
    page = int(request.args.get('page', 1))
    per_page = 10

    query = MonitoringData.query.order_by(MonitoringData.timestamp.desc())

    if status_filter:
        query = query.filter_by(status=status_filter)

    # Ambil semua data jika limit=all (tetap gunakan pagination)
    if limit == 'all':
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        monitoring_data = pagination.items
        total_data = pagination.total
        total_pages = pagination.pages
    else:
        # Ambil 50 data saja, kemudian paginate 10 per halaman
        all_limited_data = query.limit(50).all()
        total_data = len(all_limited_data)
        total_pages = (total_data + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        monitoring_data = all_limited_data[start:end]

    # Data untuk export
    export_query = query.all() if limit == 'all' else query.limit(50).all()
    data_list = [{
        "ID": d.id,
        "Timestamp": d.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        "Ketinggian": d.ketinggian_air,
        "Jarak": d.jarak_sensor,
        "Status": d.status,
        "μ Rendah": d.mu_rendah,
        "μ Sedang": d.mu_sedang,
        "μ Tinggi": d.mu_tinggi,
        "Defuzzifikasi": d.defuzzifikasi_nilai
    } for d in export_query]

    if export == "csv":
        def generate():
            header = list(data_list[0].keys()) if data_list else []
            yield ",".join(header) + "\n"
            for row in data_list:
                yield ",".join(str(row[h]) for h in header) + "\n"
        return Response(generate(), mimetype="text/csv",
                        headers={"Content-Disposition": "attachment; filename=monitoring_export.csv"})


    # elif export == "pdf":
    #     output = io.BytesIO()
    #     c = canvas.Canvas(output, pagesize=letter)
    #     width, height = letter

    #     c.setFont("Helvetica-Bold", 14)
    #     c.drawString(50, height - 40, "Laporan Monitoring Sensor")

    #     c.setFont("Helvetica", 10)
    #     y = height - 70
    #     for i, row in enumerate(data_list):
    #         line = f"{i+1}. {row['Timestamp']} | Tinggi: {row['Ketinggian']} | Status: {row['Status']}"
    #         c.drawString(50, y, line)
    #         y -= 15
    #         if y < 50:
    #             c.showPage()
    #             y = height - 50

    #     c.save()
    #     output.seek(0)
    #     return send_file(output, download_name="monitoring_export.pdf", as_attachment=True)
    elif export == "pdf":
        try:
            # Gunakan PDF generator baru
            pdf_buffer = generate_monitoring_pdf(data_list)
            return send_file(pdf_buffer, 
                           download_name=f"laporan_monitoring_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", 
                           as_attachment=True,
                           mimetype='application/pdf')
        except Exception as e:
            print(f"Error creating PDF: {e}")
            return "Error generating PDF file", 500

    return render_template('monitoring.html',
                           monitoring_data=monitoring_data,
                           selected_status=status_filter,
                           current_page=page,
                           total_pages=total_pages,
                           limit=limit)



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