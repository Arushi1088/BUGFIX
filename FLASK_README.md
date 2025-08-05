# 🌐 UX Analyzer - Flask Web Application

## 📁 Project Structure

```
ux-analyzer/
│
├── app.py                    ← ✅ Main Flask web application
├── uiux_checklist.json       ← ✅ Comprehensive UX checklist (10 categories, 98 items)
├── ux_cli.py                 ← ✅ Command-line interface (renamed from cli.py)
├── templates/
│   ├── index.html            ← ✅ Upload page with drag & drop
│   └── report.html           ← ✅ Analysis results page
├── static/
│   └── style.css             ← ✅ Professional styling
└── uploads/                  ← ✅ Temporary file storage
```

## 🎯 Features Implemented

### 🌐 Web Interface (`app.py`)
- **File Upload**: Drag & drop or click to upload screenshots
- **Real-time Analysis**: Uses OpenAI GPT-4o vision model
- **Interactive Reports**: Beautiful HTML reports with embedded screenshots
- **Export Options**: JSON export and print functionality
- **API Endpoint**: `/api/analyze` for programmatic access
- **Health Check**: `/health` endpoint for monitoring

### 🖥️ Command Line Interface (`ux_cli.py`)
- **CLI Analysis**: `python ux_cli.py screenshot.png`
- **Multiple Formats**: JSON or human-readable summary
- **File Output**: Save results to file with `-o` option
- **Comprehensive Help**: Built-in documentation and examples

### 🎨 User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Styling**: Clean, professional interface
- **Drag & Drop Upload**: Intuitive file upload experience
- **Color-coded Severity**: Visual indicators for issue priority
- **Category Grouping**: Issues organized by UX category

### 📊 Analysis Features
- **10 UX Categories**: Visual Design, Navigation, Accessibility, etc.
- **Severity Levels**: High, Medium, Low priority classification
- **Bounding Boxes**: Location coordinates when available
- **Summary Statistics**: Total issues and severity breakdown
- **Detailed Descriptions**: Specific actionable feedback

## 🚀 Usage

### Web Application
```bash
# Start the web server
source .venv/bin/activate
export OPENAI_API_KEY='your-api-key-here'
python app.py

# Visit: http://localhost:5000
```

### Command Line
```bash
# Basic analysis
python ux_cli.py screenshot.png

# Human-readable summary
python ux_cli.py screenshot.png --format summary

# Save to file
python ux_cli.py screenshot.png -o report.json
```

### API Usage
```bash
# Programmatic analysis
curl -X POST -F "file=@screenshot.png" http://localhost:5000/api/analyze
```

## 📋 Endpoints

- **`GET /`** - Upload page
- **`POST /upload`** - File upload and analysis
- **`POST /api/analyze`** - API endpoint for analysis
- **`GET /health`** - Health check

## 🔧 Configuration

### Environment Variables
- **`OPENAI_API_KEY`** - Required for analysis
- **`FLASK_ENV`** - Set to 'development' for debug mode

### File Limits
- **Max file size**: 16MB
- **Supported formats**: PNG, JPG, JPEG, GIF, BMP, WEBP

## 🛡️ Security Features
- **Secure filename handling**: Prevents path traversal
- **File validation**: Checks file types and sizes
- **Temporary storage**: Files are cleaned up after analysis
- **Input sanitization**: Prevents malicious uploads

## 📱 Responsive Design
- **Mobile-first**: Optimized for all screen sizes
- **Touch-friendly**: Large buttons and touch targets
- **Print support**: Clean print layouts
- **Accessibility**: WCAG compliant design

## 🎉 Ready for Production!

The UX Analyzer Flask application is fully functional and ready to use:

✅ **Complete web interface** with professional styling
✅ **Command-line tools** for automation
✅ **API endpoints** for integration
✅ **Comprehensive analysis** using OpenAI vision
✅ **Export capabilities** (JSON, print)
✅ **Responsive design** for all devices
✅ **Error handling** and validation
✅ **Security measures** implemented

## Next Steps
1. Set your OpenAI API key: `export OPENAI_API_KEY='your-key'`
2. Start the application: `python app.py`
3. Visit: http://localhost:5000
4. Upload a screenshot and get instant UX analysis!

🎯 **Perfect for**: UX audits, design reviews, accessibility checks, and continuous UI/UX improvement!
