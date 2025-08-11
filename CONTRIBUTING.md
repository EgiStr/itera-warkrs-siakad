# Contributing to WAR KRS SIAKAD ITERA

Terima kasih atas minat Anda untuk berkontribusi pada project WAR KRS SIAKAD ITERA! 🎉

Kami sangat menghargai kontribusi dari komunitas untuk membuat tool ini lebih baik dan bermanfaat bagi mahasiswa ITERA.

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Cara Berkontribusi](#-cara-berkontribusi)
- [Setup Development Environment](#-setup-development-environment)
- [Jenis Kontribusi](#-jenis-kontribusi)
- [Pull Request Guidelines](#-pull-request-guidelines)
- [Issue Guidelines](#-issue-guidelines)
- [Coding Standards](#-coding-standards)
- [Testing](#-testing)
- [Documentation](#-documentation)

## 🤝 Code of Conduct

Project ini mengikuti [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Dengan berpartisipasi, Anda diharapkan untuk menjunjung tinggi kode etik ini.

### Prinsip Utama:
- ✅ **Respectful**: Hormati semua kontributor terlepas dari pengalaman, gender, identitas, agama, atau latar belakang
- ✅ **Constructive**: Berikan feedback yang membangun dan solutif
- ✅ **Collaborative**: Bekerja sama untuk mencapai tujuan bersama
- ✅ **Professional**: Maintain profesionalisme dalam semua interaksi

## 🚀 Cara Berkontribusi

### 1. Fork Repository

```bash
# Fork repository di GitHub
# Kemudian clone fork Anda
git clone https://github.com/YOUR_USERNAME/itera-warkrs-siakad-2025.git
cd itera-warkrs-siakad-2025

# Tambahkan remote upstream
git remote add upstream https://github.com/EgiStr/itera-warkrs-siakad-2025.git
```

### 2. Buat Branch Baru

```bash
# Update main branch
git checkout main
git pull upstream main

# Buat branch baru untuk fitur/fix
git checkout -b feature/nama-fitur
# atau
git checkout -b fix/nama-bug
# atau
git checkout -b docs/update-documentation
```

### 3. Lakukan Perubahan

- 📝 Buat perubahan sesuai dengan issue atau fitur yang dikerjakan
- ✅ Test perubahan Anda secara menyeluruh
- 📚 Update dokumentasi jika diperlukan
- 🧪 Tambahkan test jika menambah fitur baru

### 4. Commit Changes

```bash
# Add changes
git add .

# Commit dengan pesan yang descriptive
git commit -m "feat: tambah fitur notifikasi email"
# atau
git commit -m "fix: perbaiki bug session timeout"
# atau
git commit -m "docs: update installation guide"
```

### 5. Push dan Create Pull Request

```bash
# Push ke fork Anda
git push origin feature/nama-fitur

# Buat Pull Request di GitHub
```

## 🛠️ Setup Development Environment

### Prerequisites

- Python 3.7+
- Git
- Virtual Environment (recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/EgiStr/itera-warkrs-siakad-2025.git
cd itera-warkrs-siakad-2025

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# atau
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (jika ada)
pip install -r requirements-dev.txt  # jika tersedia

# Copy dan setup environment variables
cp .env.example .env
# Edit .env dengan konfigurasi development Anda
```

### Verifikasi Setup

```bash
# Test aplikasi
python main.py --help

# Test setup configuration
python setup.py

# Run tests (jika ada)
python -m pytest
```

## 🎯 Jenis Kontribusi

Kami menerima berbagai jenis kontribusi:

### 🐛 Bug Reports
- Laporkan bug yang Anda temukan
- Sertakan langkah reproduksi yang jelas
- Include log error dan screenshot jika memungkinkan

### 💡 Feature Requests
- Usulkan fitur baru yang bermanfaat
- Jelaskan use case dan manfaatnya
- Diskusikan implementasi yang mungkin

### 🔧 Code Contributions
- **Bug fixes**: Perbaikan bug yang ada
- **New features**: Implementasi fitur baru
- **Performance improvements**: Optimasi performa
- **Refactoring**: Perbaikan struktur kode

### 📚 Documentation
- Perbaikan dokumentasi
- Penambahan contoh penggunaan
- Translate dokumentasi
- Update course list (COURSE_LIST.md)

### 🧪 Testing
- Menambah unit tests
- Integration tests
- Manual testing dan feedback

### 🎨 UI/UX Improvements
- Perbaikan user experience
- CLI interface improvements
- Error message improvements

## 📝 Pull Request Guidelines

### Before Submitting

- ✅ **Sync dengan upstream**: Pastikan branch Anda up-to-date
- ✅ **Test thoroughly**: Test semua perubahan secara menyeluruh
- ✅ **Check code style**: Ikuti coding standards yang ada
- ✅ **Update docs**: Update dokumentasi jika diperlukan
- ✅ **Small focused changes**: Satu PR untuk satu perubahan

### PR Title Format

```
<type>: <description>

Examples:
feat: tambah fitur backup konfigurasi
fix: perbaiki bug session expired
docs: update contributing guidelines
refactor: improve error handling
test: tambah unit tests untuk parser
```

### PR Description Template

```markdown
## 📋 Description
Jelaskan perubahan yang dibuat dan alasannya.

## 🔄 Changes Made
- [ ] Perubahan 1
- [ ] Perubahan 2
- [ ] Perubahan 3

## 🧪 Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] Edge cases tested

## 📚 Documentation
- [ ] README updated (if needed)
- [ ] Code comments added
- [ ] API docs updated (if needed)

## 📷 Screenshots (if applicable)
Include screenshots for UI changes

## 🔗 Related Issues
Closes #123
Related to #456
```

## 🐛 Issue Guidelines

### Creating Issues

#### Bug Report Template

```markdown
**🐛 Bug Description**
Clear description of the bug

**📋 Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**✅ Expected Behavior**
What should have happened

**❌ Actual Behavior**
What actually happened

**💻 Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.8.10]
- Application version: [e.g., 1.0.0]

**📝 Additional Context**
- Log files
- Screenshots
- Configuration details
```

#### Feature Request Template

```markdown
**💡 Feature Description**
Clear description of the proposed feature

**🎯 Problem Statement**
What problem does this solve?

**💭 Proposed Solution**
How should this be implemented?

**🔄 Alternatives Considered**
Other solutions you've considered

**📋 Additional Context**
Any other context or examples
```

## 📏 Coding Standards

### Python Code Style

Kami mengikuti [PEP 8](https://www.python.org/dev/peps/pep-0008/) dengan beberapa penyesuaian:

```python
# Import organization
import os
import sys
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from src.utils import helper_function

# Line length: 88 characters (Black formatter)
# Use type hints
def process_courses(courses: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    """Process course list and return formatted data.
    
    Args:
        courses: List of course dictionaries
        
    Returns:
        Formatted course data or None if error
    """
    pass

# Class naming: PascalCase
class KRSService:
    """Service for handling KRS operations."""
    
    def __init__(self, session: requests.Session) -> None:
        self.session = session
    
    # Method naming: snake_case
    def register_course(self, course_id: str) -> bool:
        """Register a course."""
        pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_TIMEOUT = 30
MAX_RETRY_ATTEMPTS = 3
```

### File Organization

```
src/
├── __init__.py
├── controller.py      # Main business logic
├── session.py         # HTTP session management
├── krs_service.py     # KRS-specific operations
├── parser.py          # HTML parsing utilities
├── telegram_notifier.py # Telegram integration
└── utils.py           # Utility functions

config/
├── __init__.py
└── settings.py        # Configuration management

tests/                 # Test files (jika ada)
├── __init__.py
├── test_controller.py
├── test_parser.py
└── fixtures/

docs/                  # Additional documentation
├── API.md
├── DEPLOYMENT.md
└── TROUBLESHOOTING.md
```

### Error Handling

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def safe_operation() -> Optional[str]:
    """Example of proper error handling."""
    try:
        # Operation logic here
        result = risky_operation()
        return result
    except SpecificException as e:
        logger.error(f"Specific error occurred: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
```

### Logging Standards

```python
import logging

# Use module-level logger
logger = logging.getLogger(__name__)

# Log levels:
logger.debug("Detailed debugging information")
logger.info("General information about operation")
logger.warning("Warning about potential issue")
logger.error("Error that prevents operation")
logger.critical("Critical error that may stop application")
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_parser.py

# Run with verbose output
python -m pytest -v
```

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch

from src.parser import KRSParser

class TestKRSParser:
    """Test suite for KRSParser class."""
    
    def setup_method(self):
        """Setup before each test method."""
        self.parser = KRSParser()
    
    def test_parse_course_list(self):
        """Test course list parsing."""
        # Arrange
        html_content = "<option value='123'>Test Course</option>"
        
        # Act
        result = self.parser.parse_course_options(html_content)
        
        # Assert
        assert len(result) == 1
        assert result[0]['id'] == '123'
        assert result[0]['name'] == 'Test Course'
    
    @patch('requests.get')
    def test_network_request(self, mock_get):
        """Test with mocked network request."""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>Mock content</html>"
        mock_get.return_value = mock_response
        
        # Test your function
        result = self.parser.fetch_and_parse()
        
        # Assertions
        assert result is not None
        mock_get.assert_called_once()
```

## 📚 Documentation

### Code Documentation

```python
def register_course(self, course_id: str, class_id: str) -> bool:
    """Register a course for the student.
    
    This method attempts to register a course by sending a POST request
    to the SIAKAD system with the provided course and class IDs.
    
    Args:
        course_id: The course identifier (e.g., 'IF25-40033')
        class_id: The class identifier (e.g., '35998')
        
    Returns:
        True if registration successful, False otherwise
        
    Raises:
        SessionExpiredError: If the session has expired
        NetworkError: If network request fails
        
    Example:
        >>> service = KRSService(session)
        >>> success = service.register_course('IF25-40033', '35998')
        >>> print(f"Registration successful: {success}")
    """
```

### Documentation Updates

Saat menambah fitur baru, pastikan untuk update:

- ✅ **README.md**: Fitur overview dan quick start
- ✅ **COURSE_LIST.md**: Jika ada perubahan mata kuliah
- ✅ **Code comments**: Inline documentation
- ✅ **Docstrings**: Function/class documentation
- ✅ **Examples**: Usage examples dalam docs

## 🏷️ Release Process

### Version Numbering

Menggunakan [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Tag created
- [ ] Release notes prepared

## 🆘 Getting Help

### Communication Channels

- **GitHub Issues**: Technical questions dan bug reports
- **GitHub Discussions**: General questions dan ideas
- **Pull Request Comments**: Code review discussions

### Before Asking for Help

1. **Search existing issues**: Mungkin sudah ada yang tanya
2. **Check documentation**: README, CONTRIBUTING, dan code comments
3. **Try debugging**: Enable debug logging untuk informasi lebih detail
4. **Prepare context**: Include relevant logs, config, dan steps

### When Asking for Help

- ✅ **Be specific**: Jelaskan masalah dengan detail
- ✅ **Include context**: OS, Python version, configuration
- ✅ **Show what you tried**: Steps yang sudah dicoba
- ✅ **Include logs**: Relevant error messages atau logs
- ✅ **Be patient**: Contributors volunteer, response mungkin butuh waktu

## 🎁 Recognition

### Contributors

Semua kontributor akan diakui dalam:

- **README.md**: Contributors section
- **CHANGELOG.md**: Credit untuk perubahan spesifik
- **GitHub**: Contributor graph dan stats
- **Releases**: Credit dalam release notes

### Types of Recognition

- 🏆 **Code Contributors**: Yang submit code changes
- 📚 **Documentation Contributors**: Yang improve documentations
- 🐛 **Bug Reporters**: Yang report bugs dengan detail
- 💡 **Idea Contributors**: Yang suggest valuable features
- 🧪 **Testers**: Yang help dengan testing dan QA
- 🌍 **Community Contributors**: Yang help other users

## 📋 Checklist untuk Kontributor Baru

Sebelum submit PR pertama Anda:

- [ ] **Read** seluruh contributing guidelines ini
- [ ] **Setup** development environment
- [ ] **Test** bahwa aplikasi berjalan di environment Anda
- [ ] **Pick** issue yang sesuai dengan skill level Anda
- [ ] **Ask questions** jika ada yang tidak clear
- [ ] **Start small**: Pilih issue yang tidak terlalu complex untuk PR pertama

## 🚀 Quick Start untuk Kontributor

```bash
# 1. Fork & Clone
git clone https://github.com/YOUR_USERNAME/itera-warkrs-siakad-2025.git
cd itera-warkrs-siakad-2025

# 2. Setup Environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 3. Create Branch
git checkout -b feature/my-contribution

# 4. Make Changes
# ... edit files ...

# 5. Test Changes
python main.py --help

# 6. Commit & Push
git add .
git commit -m "feat: describe your changes"
git push origin feature/my-contribution

# 7. Create Pull Request on GitHub
```

---

## 🙏 Thank You!

Terima kasih telah mempertimbangkan untuk berkontribusi pada WAR KRS SIAKAD ITERA! 

Setiap kontribusi, tidak peduli sekecil apapun, sangat berharga untuk komunitas mahasiswa ITERA. Bersama-sama kita bisa membuat tool ini lebih baik dan bermanfaat untuk semua! 🎉

---

**Questions?** Buat issue di GitHub atau start discussion di tab Discussions.

**Want to contribute?** Check out [good first issues](https://github.com/EgiStr/itera-warkrs-siakad-2025/labels/good%20first%20issue) untuk memulai!
