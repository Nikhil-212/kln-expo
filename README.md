## Legal Document Writer (Backend)

This is a Flask-based backend for generating legal documents without using transformer models. It provides endpoints for intent interpretation, clause search, draft assembly, validation, and export to DOCX/PDF.

### Features

- Classic NLP only (spaCy non-transformer, NLTK, sumy) — no transformers
- IR via Whoosh (BM25-like) for clause search
- Rule-based validation per jurisdiction and document type
- Jinja2-based document assembly with slot filling
- Export to DOCX (python-docx) and PDF (ReportLab)

### Prerequisites

- Python 3.10+
- pip

Optional for spaCy:
- Run: `python -m spacy download en_core_web_sm`

### Setup

```bash
python -m venv .venv
. .venv/Scripts/Activate  # Windows PowerShell: . .venv/Scripts/Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm  # required for spaCy pipeline (non-transformer)
```

### Run (Development)

```bash
set FLASK_APP=wsgi:app
set FLASK_ENV=development
flask run
```

Or:

```bash
python wsgi.py
```

The server runs at `http://127.0.0.1:5000`.

### Endpoints

- POST `/api/interpret`
- POST `/api/clauses/search`
- POST `/api/draft/assemble`
- POST `/api/draft/validate`
- POST `/api/draft/simplify`
- POST `/api/export/docx`
- POST `/api/export/pdf`

See inline docstrings for request/response schemas.

### Notes

- This project intentionally avoids transformers (no BERT/GPT/HF transformers).
- Data is in-memory for demo; replace with a database in production.

# 📄 Legal Document Generator

A web-based platform that generates legal documents from natural language prompts using traditional NLP methods (spaCy, regex, rule-based extraction).

## 🎯 Features

- **Natural Language Processing**: Uses spaCy for entity extraction and regex patterns for information parsing
- **Document Type Classification**: Automatically identifies document type from user prompts
- **Interactive Form Completion**: Prompts users for missing required information
- **Multiple Document Types**: Supports Rental Agreements, Land Sale Deeds, Power of Attorney, and House Leases
- **Multiple Export Formats**: Generate documents in DOCX and PDF formats
- **Modern Web Interface**: Responsive design with step-by-step workflow
- **Template-Based Generation**: Uses Jinja2 templates for professional document formatting

## 🏗️ Architecture

```
legal-doc-generator/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   └── templates/            # HTML templates
│       └── index.html        # Frontend interface
├── templates/                # Document templates
│   ├── rental_agreement_template.txt
│   ├── land_sale_deed_template.txt
│   ├── power_of_attorney_template.txt
│   └── house_lease_template.txt
├── static/                   # Static assets
├── data/                     # Data storage
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd legal-doc-generator
   ```

2. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install spaCy language model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and go to: `http://localhost:5000`

## 📋 Supported Document Types

### 1. Rental Agreement
- **Keywords**: rental, rent, lease, tenant, landlord, monthly
- **Required Fields**: landlord, tenant, address, rent_amount, start_date, duration

### 2. Land Sale Deed
- **Keywords**: sale, deed, property, buyer, seller, purchase
- **Required Fields**: seller, buyer, property_address, sale_amount, sale_date

### 3. Power of Attorney
- **Keywords**: power of attorney, attorney, authorize, representative
- **Required Fields**: principal, attorney, authority_scope, effective_date

### 4. House Lease
- **Keywords**: house, lease, residential, accommodation
- **Required Fields**: lessor, lessee, property_address, lease_amount, start_date, duration

## 💡 Example Usage

### Example 1: Rental Agreement
**Input Prompt:**
```
"Create a house rental agreement between Anjali and Rohit for a flat in Mumbai for ₹30,000 per month."
```

**System Output:**
- Document Type: Rental Agreement
- Extracted Entities:
  - Names: Anjali, Rohit
  - Roles: Anjali (Landlord), Rohit (Tenant)
  - Location: Mumbai
  - Amount: ₹30,000
- Missing Fields: start_date, duration

### Example 2: Land Sale Deed
**Input Prompt:**
```
"Generate a land sale deed between Rajesh Kumar and Priya Singh for property in Delhi worth ₹50,00,000."
```

**System Output:**
- Document Type: Land Sale Deed
- Extracted Entities:
  - Names: Rajesh Kumar, Priya Singh
  - Roles: Rajesh Kumar (Seller), Priya Singh (Buyer)
  - Location: Delhi
  - Amount: ₹50,00,000
- Missing Fields: sale_date

## 🔧 Technical Details

### NLP Processing Pipeline

1. **Document Type Classification**
   - Keyword-based scoring system
   - Rule-based classification using predefined patterns

2. **Entity Extraction**
   - **Names**: spaCy NER for person names
   - **Amounts**: Regex patterns for currency and numbers
   - **Dates**: Regex patterns for various date formats
   - **Locations**: Context-based extraction using spaCy
   - **Durations**: Regex patterns for time periods

3. **Role Assignment**
   - Context-based role assignment
   - Position-based assignment for multiple names

4. **Missing Field Detection**
   - Template-based required field validation
   - Interactive form generation for missing data

### Template System

- Uses Jinja2 templating engine
- Fallback templates for missing template files
- Professional legal document formatting
- Placeholder system for dynamic content

### File Generation

- **DOCX**: Uses python-docx library
- **PDF**: Uses pdfkit (requires wkhtmltopdf)
- **Fallback**: HTML output if PDF generation fails

## 🛠️ Configuration

### Environment Variables
```bash
# Optional: Set Flask environment
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### Customizing Templates
1. Edit template files in the `templates/` directory
2. Use Jinja2 syntax: `{{ variable_name }}`
3. Add fallback values: `{{ variable_name or "default_value" }}`

### Adding New Document Types
1. Update `document_types` in `LegalDocumentProcessor` class
2. Add keywords and required fields
3. Create corresponding template file
4. Update entity extraction patterns if needed

## 📱 API Endpoints

### POST /api/process-prompt
Process user prompt and extract information.

**Request:**
```json
{
  "prompt": "Create a rental agreement between John and Sarah for $2000 per month"
}
```

**Response:**
```json
{
  "document_type": "rental_agreement",
  "extracted_entities": {
    "names": ["John", "Sarah"],
    "amounts": ["$2000"],
    "roles": {
      "landlord": "John",
      "tenant": "Sarah"
    }
  },
  "missing_fields": ["address", "start_date", "duration"],
  "status": "success"
}
```

### POST /api/generate-document
Generate final document with all required data.

**Request:**
```json
{
  "document_type": "rental_agreement",
  "filled_data": {
    "landlord": "John",
    "tenant": "Sarah",
    "address": "123 Main St",
    "rent_amount": "$2000",
    "start_date": "01/01/2024",
    "duration": "12"
  },
  "format": "docx"
}
```

**Response:** File download (DOCX or PDF)

## 🔒 Security Considerations

- No sensitive data is stored permanently
- Temporary files are cleaned up after download
- Input validation and sanitization
- CORS enabled for development

## 🚧 Limitations

- Requires spaCy English model for NLP processing
- PDF generation requires wkhtmltopdf installation
- Limited to predefined document types
- No legal validation or compliance checking

## 🔮 Future Enhancements

- [ ] User authentication and history tracking
- [ ] Admin panel for template management
- [ ] Multi-language support (Hindi, etc.)
- [ ] Digital signature integration
- [ ] Email/WhatsApp document delivery
- [ ] More document types and templates
- [ ] Advanced NLP with custom training
- [ ] Document validation and compliance checking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section below
2. Review the API documentation
3. Create an issue in the repository

## 🔧 Troubleshooting

### Common Issues

1. **spaCy model not found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **PDF generation fails**
   - Install wkhtmltopdf: `brew install wkhtmltopdf` (macOS) or download from official website
   - The system will fallback to HTML output

3. **Port already in use**
   - Change port in `app.py`: `app.run(port=5001)`

4. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

### Performance Optimization

- For production deployment, consider using Gunicorn or uWSGI
- Enable caching for spaCy model loading
- Implement request rate limiting
- Use a production database for session management

---

**Note**: This tool is for educational and demonstration purposes. Generated documents should be reviewed by legal professionals before use in actual legal proceedings. 