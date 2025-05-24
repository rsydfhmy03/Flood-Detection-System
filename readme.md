# 🌊 Flask Flood Detection System

Sistem monitoring banjir real-time berbasis Flask dan ESP32. Menampilkan dashboard interaktif, integrasi IoT API, dan logika fuzzy untuk klasifikasi status banjir.

---

## 📋 Requirements & Dependencies

### 1. Software Requirements
- Python 3.10+
- MySQL Server
- Git (optional)

### 2. Python Libraries

Tersimpan dalam `requirements.txt`:
```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
PyMySQL==1.1.0
requests==2.31.0
numpy==1.24.3
plotly==5.15.0
Werkzeug==2.3.7
````

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### 1. Setup Database

```bash
# Buat database MySQL
mysql -u root -p
CREATE DATABASE flood_monitoring;
exit;

# Inisialisasi tabel-tabel
python create_db.py
```

### 2. Jalankan Aplikasi

```bash
python app.py
# Atau
flask run --host=0.0.0.0 --port=5000
```

---

## 🌐 Access URLs

| Fungsi        | URL                                                                                          |
| ------------- | -------------------------------------------------------------------------------------------- |
| Web Dashboard | [http://localhost:5000](http://localhost:5000)                                               |
| Login Page    | [http://localhost:5000/login](http://localhost:5000/login)                                   |
| API (ESP32)   | [http://192.168.x.x:5000/api/monitoring/store](http://192.168.x.x:5000/api/monitoring/store) |

> 🔁 Ganti `192.168.x.x` dengan IP address komputer yang menjalankan Flask.

---

## 🔧 ESP32 Configuration

Pastikan URL server pada kode ESP32 kamu sesuai:

```cpp
const char* serverURL = "http://192.168.x.x:5000/api/monitoring/store";
```

---

## 📊 Features Overview

### 🔐 Authentication

* Login/Logout menggunakan session
* Route proteksi via decorator

### 📈 Real-time Dashboard

* Grafik ketinggian air (Plotly.js)
* Status klasifikasi (Aman / Siaga / Banjir)
* Data sensor langsung dari ESP32

### 🔌 IoT API Integration

* Endpoint POST data sensor dari ESP32
* Fuzzy Logic Mamdani auto-calculate
* Data tersimpan di MySQL

### 🧠 Fuzzy Manual Calculator

* Input manual ketinggian
* Langkah per langkah:

  * Fuzzifikasi
  * Inferensi
  * Agregasi
  * Defuzzifikasi
* Grafik fungsi keanggotaan

### 📈 Data Analytics

* Grafik historis (24 jam & 2 jam)
* Tabel data terbaru
* Statistik harian

---

## 🧮 Fuzzy Logic Overview

### Membership Functions:

| Label  | Range    | Bentuk           |
| ------ | -------- | ---------------- |
| Rendah | 0–20 cm  | Triangular Left  |
| Sedang | 15–35 cm | Triangular       |
| Tinggi | 30–50 cm | Triangular Right |

### Output Classification:

| Status | Output Range |
| ------ | ------------ |
| Aman   | 0–30         |
| Siaga  | 20–60        |
| Banjir | 50–100       |

### Aturan:

```
IF Ketinggian = Rendah THEN Status = Aman
IF Ketinggian = Sedang THEN Status = Siaga
IF Ketinggian = Tinggi THEN Status = Banjir
```

---

## 🔒 Security Features

* Session-based Auth
* CSRF Protection (jika ditambahkan)
* Input validation
* SQL Injection prevention (via SQLAlchemy ORM)

---

## 📱 UI & Responsiveness

* Desain modern dengan **Tailwind CSS**
* Real-time update tanpa reload
* Layout responsif (Mobile-first)

---

## 🐛 Troubleshooting

### 🛑 Database Error

* Pastikan MySQL Service aktif
* Cek `username/password` di `config.py`
* Database `flood_monitoring` sudah dibuat?

### 🔌 ESP32 Tidak Bisa Kirim Data

* Pastikan koneksi WiFi stabil
* Cek IP Address Flask server
* Periksa firewall yang memblokir port 5000

### 📉 Chart Tidak Muncul

* Pastikan koneksi internet (Plotly CDN)
* Buka console browser (F12) untuk cek error JS

---

## ⚡ Performance Tips

* Index pada kolom `timestamp`
* Caching untuk query berat
* Pagination untuk dataset besar
* Gunakan async JS untuk update cepat

---

## 🔄 Data Flow Overview

```text
ESP32 Sensor → WiFi → Flask API → MySQL Database → Web Dashboard
                          ↓
                    Fuzzy Logic
                          ↓
                 Status Classification
```

---

## 🧪 Debug & Logs

* Cek terminal Flask untuk error log
* Gunakan `print()` atau `app.logger.debug()` untuk debug
* Gunakan `MySQL Workbench` untuk inspeksi data

---

## 🤝 Credits

Dibuat dengan ❤️ oleh \[Maba (Mahasiswa Babak Akhir) POLIJE]

---

