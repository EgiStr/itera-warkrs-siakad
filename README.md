# WAR KRS SIAKAD ITERA - Automation Tool

Aplikasi otomatis untuk melakukan pendaftaran mata kuliah (WAR KRS) di SIAKAD ITERA dengan notifikasi Telegram real-time.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**📋 [DAFTAR MATA KULIAH LENGKAP](COURSE_LIST.md) - Lihat semua mata kuliah yang tersedia dengan kode dan ID kelas**

## ✨ Features

- ✅ **Automated Course Registration**: Otomatis mendaftarkan mata kuliah secara berulang sampai berhasil
- ✅ **Anti-Detection**: Menggunakan cloudscraper untuk menghindari deteksi bot
- ✅ **Session Management**: Mengelola session dan cookies secara aman
- ✅ **Environment Variables**: Kredensial disimpan aman di file .env
- ✅ **Telegram Notifications**: Notifikasi real-time ke Telegram saat:
  - Proses dimulai
  - Mata kuliah berhasil didaftarkan
  - Semua proses selesai
  - Terjadi error atau session expired
- ✅ **Professional Architecture**: Mengikuti SOLID principles dengan clean code
- ✅ **Comprehensive Logging**: Log detail untuk debugging dan monitoring
- ✅ **Interactive Setup**: Setup wizard yang mudah digunakan

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.7+
- Access ke SIAKAD ITERA
- Telegram Bot (optional, untuk notifikasi)

### 2. Installation

```bash
# Clone atau download project
cd warkrs

# Install dependencies
pip install -r requirements.txt

# Atau gunakan virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# atau
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Setup Configuration

**📋 Sebelum setup, lihat daftar mata kuliah yang tersedia:**
**[COURSE_LIST.md](COURSE_LIST.md)** - Daftar lengkap mata kuliah dengan kode dan ID kelas

```bash
# Jalankan setup wizard
python setup.py
```

Setup wizard akan memandu Anda untuk:
1. **Cookie Setup**: Mengambil CI_SESSION dan CF_CLEARANCE dari browser
2. **Target Courses**: Mengatur mata kuliah yang ingin didaftarkan
3. **Settings**: Konfigurasi delay dan timeout
4. **Telegram Setup**: Mengatur notifikasi Telegram (optional)

### 4. Run the Application

```bash
# Check status konfigurasi
python main.py --status

# Test koneksi Telegram (jika dikonfigurasi)
python main.py --test-telegram

# Mulai automation
python main.py
```

## 📱 Telegram Notification Setup

### Membuat Telegram Bot

1. **Buka @BotFather di Telegram**
2. **Kirim command `/newbot`**
3. **Ikuti instruksi untuk membuat bot baru**
4. **Simpan Bot Token yang diberikan**

### Mendapatkan Chat ID

1. **Start chat dengan bot Anda**
2. **Kirim pesan apa saja ke bot**
3. **Buka browser dan kunjungi:**
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
   ```
4. **Cari `"chat":{"id":123456789` dan ambil angka tersebut**

### Konfigurasi di .env

```env
# Telegram Notifications
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## 🛠️ Configuration

### File Structure

```
warkrs/
├── main.py              # Entry point aplikasi
├── setup.py             # Setup wizard
├── requirements.txt     # Dependencies
├── .env                 # Environment variables (buat saat setup)
├── config/
│   ├── config.json     # Konfigurasi utama (buat saat setup)
│   └── settings.py     # Configuration management
└── src/
    ├── controller.py   # Main business logic
    ├── session.py      # HTTP session management
    ├── krs_service.py  # KRS registration service
    ├── parser.py       # HTML parsing utilities
    ├── telegram_notifier.py # Telegram notifications
    └── utils.py        # Utility functions
```

### Environment Variables (.env)

```env
# SIAKAD Authentication Cookies
CI_SESSION=your_ci_session_cookie
CF_CLEARANCE=your_cf_clearance_cookie

# Telegram Notifications (optional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Optional: Override default settings
# DELAY_SECONDS=45
# REQUEST_TIMEOUT=20
```

### Configuration (config/config.json)

```json
{
    "cookies": {
        "ci_session": "ENV:CI_SESSION",
        "cf_clearance": "ENV:CF_CLEARANCE"
    },
    "target_courses": {
        "SD25-41301": "37813",
        "SD25-40004": "37705"
    },
    "settings": {
        "delay_seconds": 45,
        "request_timeout": 20,
        "verification_delay": 2,
        "inter_request_delay": 2
    },
    "urls": {
        "pilih_mk": "https://siakad.itera.ac.id/mahasiswa/krsbaru/pilihmk",
        "simpan_krs": "https://siakad.itera.ac.id/mahasiswa/krsbaru/simpanKRS"
    }
}
```

## � Course Selection Guide

### Mencari Mata Kuliah

1. **Lihat daftar lengkap**: [COURSE_LIST.md](COURSE_LIST.md) berisi semua mata kuliah yang tersedia
2. **Cari berdasarkan program studi**: Mata kuliah dikelompokkan berdasarkan kode program (IF25, TK25, dll.)
3. **Catat kode dan class ID**: Format `"KODE_MATA_KULIAH": "CLASS_ID"`

### Format Target Courses

```json
{
    "target_courses": {
        "SD25-41301": "37813",    // Swarm Intelligence - R
        "IF25-40033": "35998",    // Tugas Akhir - R
        "TK25-40001": "36847",    // Perancangan Pabrik Kimia - RA
        "MA25-21302": "37636"     // Teori Graf - R
    }
}
```

### Tips Memilih Mata Kuliah

- ✅ **Cek prasyarat**: Pastikan sudah memenuhi mata kuliah prasyarat
- ✅ **Perhatikan jadwal**: Hindari bentrok jadwal antar mata kuliah  
- ✅ **Cek kapasitas kelas**: Beberapa kelas memiliki kapasitas terbatas
- ✅ **Prioritas tinggi**: Letakkan mata kuliah penting di urutan atas

### Manual Course ID Lookup

Jika mata kuliah tidak ada di daftar:

1. **Login ke SIAKAD ITERA**
2. **Buka halaman KRS**
3. **Inspect Element** (F12) pada dropdown mata kuliah
4. **Cari tag**: `<option value="CLASS_ID">KODE - Nama - Kelas</option>`
5. **Salin CLASS_ID**: Gunakan value di dalam option tag

**Contoh:**
```html
<option value="37813">SD25-41301 - Swarm Intelligence - R</option>
```
→ Class ID: `37813`

## �🔧 Command Line Options

```bash
# Tampilkan help
python main.py --help

# Cek status konfigurasi
python main.py --status

# Test koneksi Telegram
python main.py --test-telegram

# Setup configuration
python main.py --setup

# Custom config file
python main.py --config path/to/config.json

# Custom log level
python main.py --log-level DEBUG

# Save logs to file
python main.py --log-file logs/warkrs.log
```

## 🔒 Security Best Practices

1. **Never commit .env file** - File .env sudah ditambahkan ke .gitignore
2. **Regenerate cookies periodically** - Session cookies expire overtime
3. **Use strong Telegram bot tokens** - Keep bot token secret
4. **Limit bot permissions** - Bot hanya perlu akses kirim pesan
5. **Monitor bot usage** - Check bot activity via @BotFather

## 🐛 Troubleshooting

### Common Issues

**1. "ModuleNotFoundError"**
```bash
# Install dependencies
pip install -r requirements.txt
```

**2. "Session expired" / "Unauthorized"**
```bash
# Update cookies di .env file
# Atau jalankan setup ulang
python setup.py
```

**3. "Telegram connection failed"**
```bash
# Test koneksi
python main.py --test-telegram

# Periksa BOT_TOKEN dan CHAT_ID di .env
```

**4. "Configuration not found"**
```bash
# Jalankan setup wizard
python setup.py
```

**5. "KRS table not found" atau "No courses found"**
```bash
# Run debug mode untuk analisis HTML
python main.py --debug

# Atau gunakan debug helper script
./debug.sh

# Manual debug test
python debug_test.py
```

### Debug dan Troubleshooting

**Debug Mode:**
```bash
# Enable debug mode (saves HTML content)
python main.py --debug

# Debug logging dengan file output
python main.py --log-level DEBUG --log-file debug.log

# Quick debug test
python debug_test.py

# Run debug helper script
./debug.sh
```

**Debug Files yang Dihasilkan:**
- `debug_enrolled_courses.html` - HTML content dari halaman KRS
- `debug_full_analysis.html` - Analisis lengkap struktur halaman
- `debug.log` - Log file dengan informasi detail

**Jika Tidak Ada Mata Kuliah Ditemukan:**
1. ✅ **Cek cookies**: Pastikan CI_SESSION dan CF_CLEARANCE masih valid
2. ✅ **Cek login**: Login manual ke SIAKAD untuk verifikasi akses
3. ✅ **Cek HTML structure**: Buka debug HTML files untuk melihat struktur
4. ✅ **Update cookies**: Jika expired, ambil cookies baru dari browser
5. ✅ **Check logs**: Lihat log files untuk error details

### Getting Debug Information

```bash
# Check configuration status
python main.py --status

# Test Telegram connection
python main.py --test-telegram

# Run dengan debug logging
python main.py --log-level DEBUG --log-file debug.log
```

## 📝 Changelog

### v1.0.0
- ✅ Initial release with professional architecture
- ✅ Environment variable security
- ✅ Telegram notification integration
- ✅ Interactive setup wizard
- ✅ Comprehensive error handling
- ✅ SOLID principles implementation

## ⚠️ Disclaimer

Tool ini dibuat untuk tujuan edukasi dan membantu mahasiswa ITERA dalam proses pendaftaran KRS. Gunakan dengan bijak dan ikuti kebijakan yang berlaku di Institut Teknologi Sumatera.

## 🤝 Contributing

Kami menyambut kontribusi dari komunitas! Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan lengkap cara berkontribusi:

- 🐛 **Bug Reports**: Laporkan bug yang Anda temukan
- 💡 **Feature Requests**: Usulkan fitur baru yang bermanfaat  
- 🔧 **Code Contributions**: Submit code improvements
- 📚 **Documentation**: Bantu improve dokumentasi
- 📋 **Course List Updates**: Update daftar mata kuliah terbaru

**Quick Start untuk Kontributor:**
1. Fork repository ini
2. Buat branch untuk perubahan Anda
3. Submit Pull Request dengan deskripsi yang jelas

## 📄 License

This project is for educational purposes. Please respect your institution's policies and terms of service.

---

**Happy Coding! 🚀**

Jika ada pertanyaan atau butuh bantuan, silakan buka issue di repository ini.
