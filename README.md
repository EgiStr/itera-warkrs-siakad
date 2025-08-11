# WAR KRS SIAKAD ITERA 🎯

**Automation tool untuk War KRS (Kartu Rencana Studi) di SIAKAD Institut Teknologi Sumatera**

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🌟 Features

- ✅ **Otomatis Registration**: Mendaftarkan mata kuliah secara otomatis
- 🔄 **Continuous Monitoring**: Bruteforce registration sampai berhasil
- 🛡️ **Session Management**: Aman dengan cloudscraper anti-detection
- ⚙️ **Configurable**: Konfigurasi mudah melalui JSON dan Environment Variables
- � **Secure**: Environment variables untuk data sensitif (cookies)
- �📊 **Real-time Status**: Monitor progress secara real-time
-  **Logging**: Comprehensive logging untuk debugging
- 🎯 **Interactive Setup**: Setup wizard untuk konfigurasi mudah

## 🚀 Quick Start

### Prerequisites

- Python 3.7 atau lebih tinggi
- Akun SIAKAD ITERA yang valid
- Browser untuk mendapatkan cookies

### Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/war-krs-itera.git
   cd war-krs-itera
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup konfigurasi**
   ```bash
   python main.py --setup
   ```

### Configuration

1. **Setup Environment Variables (Recommended - Secure)**
   ```bash
   # Option 1: Use interactive setup wizard
   python setup.py
   
   # Option 2: Manual setup
   cp .env.example .env
   # Edit .env file with your credentials
   ```

2. **Get Authentication Cookies**
   - Login ke [SIAKAD ITERA](https://siakad.itera.ac.id)
   - Tekan `F12` → `Application` → `Cookies` → `https://siakad.itera.ac.id`
   - Copy nilai `ci_session` dan `cf_clearance`
   - Paste ke file `.env`:
     ```env
     CI_SESSION=your_session_here
     CF_CLEARANCE=your_clearance_here
     ```

3. **Configure Target Courses**
   Edit `config/config.json`:
   ```json
   {
     "target_courses": {
       "SD25-41301": "37704",
       "SD25-40004": "37705"
     }
   }
   ```

4. **Get Course IDs**
   - Buka halaman [Pilih Mata Kuliah](https://siakad.itera.ac.id/mahasiswa/krsbaru/pilihmk)
   - Inspect element dropdown mata kuliah
   - Copy `value` dari `<option value="12345">KODE - NAMA MK</option>`

## 🎮 Usage

### Basic Usage
```bash
python main.py
```

### Interactive Setup (Recommended)
```bash
python setup.py
```
The setup wizard will guide you through:
- 🍪 Cookie configuration
- 🎯 Target course setup  
- ⚙️ Settings configuration
- 🔒 Secure .env file creation

### Advanced Options
```bash
# Interactive setup wizard
python setup.py

# Check configuration status
python main.py --status

# Custom config file
python main.py --config my_config.json

# Enable debug logging
python main.py --log-level DEBUG

# Save logs to file
python main.py --log-file logs/war_krs.log

# Show setup guide
python main.py --setup
```

## 📁 Project Structure

```
war-krs-itera/
├── main.py                 # Entry point aplikasi
├── setup.py                # Interactive setup wizard
├── requirements.txt        # Python dependencies
├── README.md              # Dokumentasi
├── .env.example           # Template environment variables
├── .env                   # Environment variables (auto-ignored)
├── config/
│   ├── __init__.py
│   ├── settings.py        # Configuration manager
│   └── config.json        # Configuration file
└── src/
    ├── __init__.py
    ├── controller.py      # Main controller (orchestrator)
    ├── krs_service.py     # Core KRS business logic
    ├── session.py         # Session management
    ├── parser.py          # HTML parsing utilities
    └── utils.py           # Utility functions
```

## 🏗️ Architecture

Aplikasi ini mengikuti **SOLID Principles** dan **Clean Architecture**:

- **Single Responsibility**: Setiap class memiliki satu tanggung jawab
- **Open/Closed**: Mudah di-extend tanpa modifikasi
- **Liskov Substitution**: Interface yang konsisten
- **Interface Segregation**: Interface yang spesifik
- **Dependency Inversion**: Bergantung pada abstraksi

### Core Components

1. **Controller** (`controller.py`): Orchestrates the entire WAR KRS process
2. **KRSService** (`krs_service.py`): Handles KRS-specific business logic
3. **SiakadSession** (`session.py`): Manages authentication and HTTP requests
4. **KRSParser** (`parser.py`): Parses HTML content from SIAKAD
5. **Config** (`settings.py`): Manages application configuration

## ⚙️ Configuration Options

| Setting | Environment Variable | Description | Default |
|---------|---------------------|-------------|---------|
| `cookies.ci_session` | `CI_SESSION` | Session cookie dari SIAKAD | Required |
| `cookies.cf_clearance` | `CF_CLEARANCE` | Cloudflare clearance cookie | Required |
| `delay_seconds` | `DELAY_SECONDS` | Jeda antar siklus (detik) | 45 |
| `request_timeout` | `REQUEST_TIMEOUT` | Timeout HTTP request (detik) | 20 |
| `verification_delay` | - | Jeda verifikasi (detik) | 2 |
| `inter_request_delay` | - | Jeda antar request (detik) | 2 |

### Environment Variables Priority
1. **Environment variables** (highest priority)
2. **JSON configuration** (config.json)
3. **Default values** (lowest priority)

## 🛡️ Security & Best Practices

### Environment Variables
- **Gunakan .env file** untuk data sensitif (cookies)
- **Never commit .env** ke version control
- **.env sudah ada di .gitignore** secara otomatis
- **Copy dari .env.example** untuk setup awal

### Production Setup
```bash
# Clone repository
git clone https://github.com/yourusername/war-krs-itera.git
cd war-krs-itera

# Setup environment
pip install -r requirements.txt
cp .env.example .env

# Edit .env dengan credentials Anda
nano .env

# Run aplikasi
python main.py
```

### Security Guidelines
- **Regular cookie refresh** untuk session yang aman
- **Rate limiting** untuk mencegah IP blocking
- **Proper error handling** untuk stabilitas
- **Secure storage** credentials di environment variables

## 🐛 Troubleshooting

### Common Issues

1. **"Konfigurasi cookie belum diatur"**
   - Pastikan `ci_session` dan `cf_clearance` sudah diisi
   - Cookie harus dari session yang valid

2. **"Session expired"**
   - Login ulang dan update cookies
   - Periksa apakah cookies masih valid

3. **"Kuota penuh"**
   - Normal behavior, aplikasi akan terus mencoba
   - Sesuaikan `delay_seconds` jika perlu

4. **"Connection timeout"**
   - Periksa koneksi internet
   - Tingkatkan `request_timeout`

### Debug Mode
```bash
python main.py --log-level DEBUG --log-file debug.log
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines

- Follow **PEP 8** style guide
- Add **type hints** untuk semua functions
- Write **comprehensive docstrings**
- Add **unit tests** untuk new features
- Maintain **SOLID principles**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

- Tool ini dibuat untuk tujuan **edukasi** dan **otomatisasi personal**
- Gunakan dengan **bijak** dan **bertanggung jawab**
- **Tidak bertanggung jawab** atas penyalahgunaan
- Pastikan mematuhi **Terms of Service** SIAKAD ITERA

## 📞 Support

- 🐛 **Bug Reports**: [Issues](https://github.com/yourusername/war-krs-itera/issues)
- 💡 **Feature Requests**: [Issues](https://github.com/yourusername/war-krs-itera/issues)
- 📧 **Contact**: your.email@example.com

## 🙏 Acknowledgments

- Institut Teknologi Sumatera
- Python Community
- Contributors dan beta testers

---

**⭐ Star repository ini jika bermanfaat!**

Made with ❤️ by Indonesian Students
