# RegressionLab

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.8.0-blue.svg)](https://github.com/DOKOS-TAYOS/RegressionLab)

**RegressionLab** is a powerful and user-friendly curve fitting application designed for scientists, engineers, students, and data analysts. Perform curve fitting operations using multiple mathematical models with an intuitive interface.

## 🌟 Features

- **Dual Interface**: Web version (Streamlit) and desktop version (Tkinter)
- **Multiple Fitting Functions**: Linear, polynomial, trigonometric, logarithmic, inverse, hyperbolic, and custom functions
- **Multiple Operation Modes**: Normal fitting, multiple datasets, checker mode, and total fitting
- **Professional Visualization**: Publication-ready plots with error bars and customizable styles
- **Uncertainty Handling**: Automatic detection and visualization of measurement uncertainties
- **Batch Processing**: Fit multiple datasets or test all equations simultaneously
- **Internationalization**: Full support for English and Spanish (easily extensible)
- **Highly Configurable**: Customize every aspect through the `.env` file


## 📖 Documentation

Complete documentation is available in the [`docs/`](docs/) directory:

- **[Getting Started](docs/index.md)** - Main documentation index
- **[Introduction](docs/introduction.md)** - Project overview and benefits
- **[Installation Guide](docs/installation.md)** - Detailed installation instructions
- **[User Guide](docs/usage.md)** - How to use RegressionLab
- **[Configuration](docs/configuration.md)** - Configuration options
- **[API Documentation](docs/api/index.md)** - Technical reference for developers

## 🚀 Quick Start

### Web Version (Easiest)

Access RegressionLab instantly in your browser:

**[https://regressionlab.streamlit.app/](https://regressionlab.streamlit.app/)**

No installation required!

### Desktop Installation

**Quick Installation (Recommended):**

**Windows:**
```batch
install.bat
```

**Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

**Manual Installation:**

1. Clone the repository:
   ```bash
   git clone https://github.com/DOKOS-TAYOS/RegressionLab.git
   cd RegressionLab
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   # Desktop version (Tkinter)
   python -m src.main_program

   # Web version (Streamlit)
   streamlit run src/streamlit_app/app.py
   ```


## 📊 Use Cases

- **Academic Research**: Analyzing experimental data from physics, chemistry, or biology labs
- **Engineering**: Calibration curve generation, system identification, and modeling
- **Data Science**: Exploratory data analysis and model validation
- **Education**: Learning about mathematical functions and curve fitting concepts

## 🛠️ Requirements

- Python 3.10 or higher
- Windows 10/11, macOS 10.14+, or Linux
- 4 GB RAM minimum (8 GB recommended)

## 📦 Dependencies

Core dependencies:
- NumPy >= 2.0
- Matplotlib >= 3.10
- SciPy >= 1.17
- Pandas >= 2.3
- OpenPyXL >= 3.1
- Python-dotenv >= 1.0
- Colorama >= 0.4

Optional dependencies:
- Streamlit (for web interface)
- Tkinter (usually included with Python)

## 🔧 Configuration

RegressionLab is highly configurable through the `.env` file. See the [Configuration Guide](docs/configuration.md) for all available options.

Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
```

## 🤝 Contributing

Contributions are welcome! Please read the [Contributing Guidelines](docs/contributing.md) for details on:
- Development setup
- Code standards
- Pull request process

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Alejandro Mata Ali**

- Email: alejandro.mata.ali@gmail.com
- GitHub: [@DOKOS-TAYOS](https://github.com/DOKOS-TAYOS)

## 🔗 Links

- **Web Application**: [https://regressionlab.streamlit.app/](https://regressionlab.streamlit.app/)
- **GitHub Repository**: [https://github.com/DOKOS-TAYOS/RegressionLab](https://github.com/DOKOS-TAYOS/RegressionLab)
- **Issue Tracker**: [https://github.com/DOKOS-TAYOS/RegressionLab/issues](https://github.com/DOKOS-TAYOS/RegressionLab/issues)

## 💡 Need Help?

1. Check the [User Guide](docs/usage.md) for basic usage
2. Review the [Troubleshooting Guide](docs/troubleshooting.md) for common issues
3. Consult the [API Documentation](docs/api/index.md) for technical details
4. Open an issue on GitHub

---

**Version**: 0.8.0  
**Last Updated**: January 2026
