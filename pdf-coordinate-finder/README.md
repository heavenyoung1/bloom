# 🔍 PDF Coordinate Finder

Visual tool for determining field coordinates in PDF documents. Helps you quickly find coordinates (X, Y) for programmatic PDF template filling.

![PDF Coordinate Finder](https://img.shields.io/badge/PDF-Coordinate%20Finder-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 📄 **Load PDF and Images** - work with PDF files or template screenshots
- 🖱️ **Visual Coordinate Selection** - simply click on the desired locations
- 📋 **Automatic JSON Generation** - ready-to-use config for your project
- 🎯 **Precise Coordinates** - automatic conversion to PDF coordinate system
- 🔄 **Field Management** - add, remove, edit fields
- 💾 **Export Configuration** - copy JSON with one click

## 🚀 Quick Start

### Option 1: Local Run

1. Download or clone the repository
2. Open `index.html` in your browser
3. That's it! No dependencies required

### Option 2: GitHub Pages

Simply open: `https://your-username.github.io/pdf-coordinate-finder/`

## 📖 How to Use

1. **Load Template**
   - Click "Choose File"
   - Upload your PDF or template image

2. **Determine Coordinates**
   - Click on the location where you want to insert data
   - Enter field name (e.g., `inn`, `name`, `paid`)
   - Coordinates will appear automatically

3. **Copy Config**
   - Click "Copy JSON"
   - Paste into your config file

## 📋 Usage Example

### Step 1: Load PDF Template

![File Upload](docs/step1.png)

### Step 2: Click on Desired Locations

![Coordinate Selection](docs/step2.png)

### Step 3: Get JSON Config

```json
{
  "template_name": "invoice_template",
  "template_path": "templates/payment/invoice_template.pdf",
  "page_number": 0,
  "fields": {
    "static": {
      "inn": {
        "x": 100,
        "y": 700,
        "width": 150,
        "height": 15,
        "font_size": 10,
        "font_name": "Helvetica"
      }
    },
    "dynamic": {
      "name": {
        "x": 50,
        "y": 500,
        "width": 400,
        "height": 30,
        "font_size": 11,
        "font_name": "Helvetica"
      }
    }
  }
}
```

## 🎯 PDF Coordinate System

It's important to understand the PDF coordinate system:

- **Origin (0, 0)**: bottom-left corner of the page
- **X-axis**: grows to the right
- **Y-axis**: grows upward
- **A4 Size**: 595 x 842 points (width x height)
- **Unit**: points, 1 point = 1/72 inch

## 🛠️ Technologies

- **HTML5** - structure
- **CSS3** - styling
- **JavaScript** - logic
- **PDF.js** - PDF rendering (CDN)

## 📦 Project Structure

```
pdf-coordinate-finder/
├── index.html          # Main utility file
├── README.md           # Documentation
├── LICENSE             # License
└── .gitignore          # Git ignore file
```

## 🔧 Configuration

### Changing Static Fields List

In `index.html`, find the line:

```javascript
const staticFieldNames = ['inn', 'kpp', 'index_address', 'address', 'bank_account', 'correspondent_account', 'bik', 'bank_recipient'];
```

Add or remove fields as needed.

### Changing Page Size

By default, A4 (595 x 842 points) is used. To change, find:

```javascript
const pdfX = (x / canvas.width) * 595;
const pdfY = 842 - ((y / canvas.height) * 842);
```

Replace `595` and `842` with your desired dimensions.

## 📝 License

MIT License - feel free to use in any projects.

## 🤝 Contributing

Contributions are welcome! Feel free to open Issues and Pull Requests.

## ⭐ Acknowledgments

- [PDF.js](https://mozilla.github.io/pdf.js/) - for the excellent PDF library
- All project contributors

## 📞 Support

If you have questions or suggestions:
- Open an Issue in the repository
- Write in Discussions

---

**Made with ❤️ for developers**
