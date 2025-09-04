
from flask import Flask, render_template, request, send_file, flash
from string import Template
import os
import spacy
from app.services.processor import LegalDocumentProcessor
import tempfile

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-here'  # Change this in production
nlp = spacy.load('en_core_web_sm')
processor = LegalDocumentProcessor()

documents = {
    'rental_agreement': {
        'template': 'rental_agreement_template.txt',
        'fields': ['landlord', 'tenant', 'address', 'rent_amount', 'start_date', 'duration']
    },
    'land_sale_deed': {
        'template': 'land_sale_deed_template.txt',
        'fields': ['seller', 'buyer', 'property_address', 'sale_amount', 'sale_date']
    },
    'power_of_attorney': {
        'template': 'power_of_attorney_template.txt',
        'fields': ['principal', 'attorney', 'authority_scope', 'effective_date']
    },
    'house_lease': {
        'template': 'house_lease_template.txt',
        'fields': ['lessor', 'lessee', 'property_address', 'lease_amount', 'start_date', 'duration']
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/document/<doc_type>')
def document_form(doc_type):
    if doc_type not in documents:
        return render_template('index.html', error='Invalid document type')
    return render_template('document_form.html', doc_type=doc_type, fields=documents[doc_type]['fields'])

@app.route('/generate', methods=['POST'])
def generate_document():
    doc_type = request.form.get('doc_type')
    if not doc_type or doc_type not in documents:
        return render_template('index.html', error='Invalid document type')

    # Collect field values and check for missing ones
    fields = documents[doc_type]['fields']
    data = {field: request.form.get(field, '').strip() for field in fields}
    missing_fields = [field for field, value in data.items() if not value]

    if missing_fields:
        error_msg = f"Please fill in all required fields: {', '.join(missing_fields)}"
        return render_template('document_form.html', doc_type=doc_type, fields=fields, error=error_msg, values=data)

    try:
        document = processor.generate_document(doc_type, data)
        # Use spaCy to extract entities
        doc_nlp = nlp(document)
        entities = [(ent.text, ent.label_) for ent in doc_nlp.ents]
        return render_template('view_document.html', doc_type=doc_type, content=document, entities=entities)
    except Exception as e:
        return render_template('index.html', error=f'Error generating document: {str(e)}')

@app.route('/generate_from_prompt', methods=['POST'])
def generate_from_prompt():
    prompt = request.form.get('prompt', '').strip()
    if not prompt:
        flash('Please enter a prompt describing the document you want to generate.', 'error')
        return render_template('index.html')

    try:
        # Classify document type
        doc_type = processor.classify_document_type(prompt)
        if not doc_type:
            flash('Could not determine document type from your prompt. Please try rephrasing.', 'error')
            return render_template('index.html')

        # Extract entities
        entities = processor.extract_entities(prompt)

        # Generate document
        document = processor.generate_document(doc_type, entities)

        # Extract entities from generated document for display
        doc_nlp = nlp(document)
        extracted_entities = [(ent.text, ent.label_) for ent in doc_nlp.ents]

        flash(f'Document type classified as: {doc_type.replace("_", " ").title()}', 'success')
        return render_template('view_document.html', doc_type=doc_type, content=document, entities=extracted_entities, prompt=prompt)

    except Exception as e:
        flash(f'Error generating document: {str(e)}', 'error')
        return render_template('index.html')

@app.route('/download/<doc_type>/<format>')
def download_document(doc_type, format):
    # This would need the document content stored in session or database
    # For now, return a placeholder
    flash('Download functionality will be implemented with proper session management.', 'info')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
