from app import create_app

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    def __init__(self):
        self.document_types = {
            'rental_agreement': {
                'keywords': ['rental', 'rent', 'lease', 'tenant', 'landlord', 'monthly'],
                'required_fields': ['landlord', 'tenant', 'address', 'rent_amount', 'start_date', 'duration'],
                'template': 'rental_agreement_template.txt'
            },
            'land_sale_deed': {
                'keywords': ['sale', 'deed', 'property', 'buyer', 'seller', 'purchase'],
                'required_fields': ['seller', 'buyer', 'property_address', 'sale_amount', 'sale_date'],
                'template': 'land_sale_deed_template.txt'
            },
            'power_of_attorney': {
                'keywords': ['power of attorney', 'attorney', 'authorize', 'representative'],
                'required_fields': ['principal', 'attorney', 'authority_scope', 'effective_date'],
                'template': 'power_of_attorney_template.txt'
            },
            'house_lease': {
                'keywords': ['house', 'lease', 'residential', 'accommodation'],
                'required_fields': ['lessor', 'lessee', 'property_address', 'lease_amount', 'start_date', 'duration'],
                'template': 'house_lease_template.txt'
            }
        }
        
        self.entity_patterns = {
            'names': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'amounts': r'₹\s*\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:rupees?|rs?)',
            'dates': r'\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}',
            'locations': r'\b(?:in|at|located in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            'durations': r'\d+\s*(?:months?|years?|days?)'
        }
    
    def classify_document_type(self, prompt):
        """Classify document type based on keywords in the prompt"""
        prompt_lower = prompt.lower()
        scores = {}
        
        for doc_type, config in self.document_types.items():
            score = sum(1 for keyword in config['keywords'] if keyword in prompt_lower)
            scores[doc_type] = score
        
        # Return the document type with highest score
        if scores:
            return max(scores, key=scores.get)
        return 'rental_agreement'  # Default fallback
    
    def extract_entities(self, prompt):
        """Extract entities using spaCy and regex patterns"""
        doc = nlp(prompt)
        entities = {
            'names': [],
            'amounts': [],
            'dates': [],
            'locations': [],
            'durations': [],
            'roles': {},
            'addresses': [],
            'ages': [],
            'father_names': []
        }
        
        # Extract names using spaCy
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                entities['names'].append(ent.text)
        
        # Extract amounts using regex
        amount_matches = re.findall(self.entity_patterns['amounts'], prompt, re.IGNORECASE)
        entities['amounts'] = [match.strip() for match in amount_matches]
        
        # Extract dates
        date_matches = re.findall(self.entity_patterns['dates'], prompt)
        entities['dates'] = date_matches
        
        # Extract locations
        location_matches = re.findall(self.entity_patterns['locations'], prompt, re.IGNORECASE)
        entities['locations'] = location_matches
        
        # Extract durations
        duration_matches = re.findall(self.entity_patterns['durations'], prompt, re.IGNORECASE)
        entities['durations'] = duration_matches
        
        # Extract ages
        age_matches = re.findall(r'(\d+)\s*years?\s*old|aged\s*(\d+)', prompt, re.IGNORECASE)
        for match in age_matches:
            age = match[0] if match[0] else match[1]
            entities['ages'].append(age)
        
        # Extract father names (S/o pattern)
        father_matches = re.findall(r'S/o\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', prompt, re.IGNORECASE)
        entities['father_names'] = father_matches
        
        # Extract addresses
        address_matches = re.findall(r'No\.\s*([^,]+),?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*-\s*(\d{6})', prompt, re.IGNORECASE)
        entities['addresses'] = address_matches
        
        # Determine roles based on context
        self._assign_roles(entities, prompt)
        
        return entities
    
    def _assign_roles(self, entities, prompt):
        """Assign roles to extracted names based on context"""
        prompt_lower = prompt.lower()
        
        if 'rental' in prompt_lower or 'lease' in prompt_lower:
            if len(entities['names']) >= 2:
                entities['roles']['landlord'] = entities['names'][0]
                entities['roles']['tenant'] = entities['names'][1]
                # Assign additional details if available
                if entities['ages']:
                    entities['roles']['landlord_age'] = entities['ages'][0] if len(entities['ages']) > 0 else '35'
                    entities['roles']['tenant_age'] = entities['ages'][1] if len(entities['ages']) > 1 else '30'
                if entities['father_names']:
                    entities['roles']['landlord_father'] = entities['father_names'][0] if len(entities['father_names']) > 0 else 'Father Name'
                    entities['roles']['tenant_father'] = entities['father_names'][1] if len(entities['father_names']) > 1 else 'Father Name'
        
        elif 'sale' in prompt_lower or 'deed' in prompt_lower:
            if len(entities['names']) >= 2:
                entities['roles']['seller'] = entities['names'][0]
                entities['roles']['buyer'] = entities['names'][1]
                # Assign additional details if available
                if entities['ages']:
                    entities['roles']['seller_age'] = entities['ages'][0] if len(entities['ages']) > 0 else '45'
                    entities['roles']['buyer_age'] = entities['ages'][1] if len(entities['ages']) > 1 else '40'
                if entities['father_names']:
                    entities['roles']['seller_father'] = entities['father_names'][0] if len(entities['father_names']) > 0 else 'Father Name'
                    entities['roles']['buyer_father'] = entities['father_names'][1] if len(entities['father_names']) > 1 else 'Father Name'
        
        elif 'power of attorney' in prompt_lower:
            if len(entities['names']) >= 2:
                entities['roles']['principal'] = entities['names'][0]
                entities['roles']['attorney'] = entities['names'][1]
                # Assign additional details if available
                if entities['ages']:
                    entities['roles']['principal_age'] = entities['ages'][0] if len(entities['ages']) > 0 else '50'
                    entities['roles']['attorney_age'] = entities['ages'][1] if len(entities['ages']) > 1 else '35'
                if entities['father_names']:
                    entities['roles']['principal_father'] = entities['father_names'][0] if len(entities['father_names']) > 0 else 'Father Name'
                    entities['roles']['attorney_father'] = entities['father_names'][1] if len(entities['father_names']) > 1 else 'Father Name'
    
    def identify_missing_fields(self, doc_type, extracted_entities):
        """Identify missing required fields for the document type"""
        required_fields = self.document_types[doc_type]['required_fields']
        missing_fields = []
        
        for field in required_fields:
            if field not in extracted_entities or not extracted_entities[field]:
                missing_fields.append(field)
        
        return missing_fields
    
    def generate_document(self, doc_type, filled_data, language: str = 'en'):
        """Generate document using template and filled data.
        If a language-specific template exists under templates/<language>/, it will be used.
        Fallback to templates/ root if not present.
        """
        # Try language-specific template first
        lang_template_path = os.path.join('templates', language, self.document_types[doc_type]['template'])
        default_template_path = os.path.join('templates', self.document_types[doc_type]['template'])
        
        # Add default values for realistic templates
        default_data = self._get_default_data(doc_type)
        filled_data = {**default_data, **filled_data}
        
        try:
            template_path = lang_template_path if os.path.exists(lang_template_path) else default_template_path
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            template = Template(template_content)
            document_content = template.render(**filled_data)
            
            return document_content
        except FileNotFoundError:
            # Fallback template
            return self._generate_fallback_template(doc_type, filled_data)
    
    def _get_default_data(self, doc_type):
        """Get default data for realistic templates"""
        from datetime import datetime
        current_date = datetime.now()
        
        defaults = {
            'date': current_date.strftime('%d'),
            'month': current_date.strftime('%B'),
            'year': current_date.strftime('%Y'),
            'execution_date': current_date.strftime('%d/%m/%Y'),
            'execution_place': 'Chennai',
            'witness1_name': 'Mr. Witness One',
            'witness1_address': 'No. 123, Main Street, Chennai - 600001',
            'witness2_name': 'Mr. Witness Two', 
            'witness2_address': 'No. 456, Second Street, Chennai - 600002',
            'jurisdiction': 'Chennai',
            'registration_office': 'Chennai',
            'stamp_duty_bearer': 'Vendee'
        }
        
        if doc_type == 'rental_agreement':
            defaults.update({
                'landlord_age': '45',
                'tenant_age': '35',
                'landlord_father': 'Father Name',
                'tenant_father': 'Father Name',
                'landlord_address': 'No. 123, Main Street',
                'landlord_city': 'Chennai',
                'landlord_pincode': '600001',
                'tenant_address': 'No. 456, Second Street',
                'tenant_city': 'Chennai',
                'tenant_pincode': '600002',
                'property_address': 'No. 789, Property Street',
                'property_city': 'Chennai',
                'property_pincode': '600073',
                'start_date': '1st April 2024',
                'effective_date': '1st April 2024',
                'duration': '11',
                'renewal_period': '11',
                'rent_amount': '15,000',
                'rent_amount_words': 'Fifteen Thousand',
                'rent_due_date': '1st',
                'rent_increase_percentage': '10',
                'security_deposit': '30,000',
                'security_deposit_words': 'Thirty Thousand',
                'notice_period': '2'
            })
        elif doc_type == 'land_sale_deed':
            defaults.update({
                'seller_age': '50',
                'buyer_age': '40',
                'seller_father': 'Father Name',
                'buyer_father': 'Father Name',
                'seller_address': 'No. 123, Main Street',
                'seller_city': 'Chennai',
                'seller_pincode': '600001',
                'buyer_address': 'No. 456, Second Street',
                'buyer_city': 'Chennai',
                'buyer_pincode': '600002',
                'property_address': 'No. 789, Property Street',
                'property_city': 'Chennai',
                'property_pincode': '600073',
                'sale_amount': '50,00,000',
                'sale_amount_words': 'Fifty Lakhs',
                'sale_date': '1st April 2024',
                'survey_number': '123/45',
                'area': '2400',
                'north_boundary': 'Main Road',
                'south_boundary': 'Residential Area',
                'east_boundary': 'Park',
                'west_boundary': 'Commercial Area'
            })
        elif doc_type == 'power_of_attorney':
            defaults.update({
                'principal_age': '55',
                'attorney_age': '40',
                'principal_father': 'Father Name',
                'attorney_father': 'Father Name',
                'principal_address': 'No. 123, Main Street',
                'principal_city': 'Chennai',
                'principal_pincode': '600001',
                'attorney_address': 'No. 456, Second Street',
                'attorney_city': 'Chennai',
                'attorney_pincode': '600002',
                'matter_description': 'property management and legal representation',
                'effective_date': '1st April 2024',
                'expiry_date': '31st March 2025'
            })
        elif doc_type == 'house_lease':
            defaults.update({
                'lessor_age': '50',
                'lessee_age': '35',
                'lessor_father': 'Father Name',
                'lessee_father': 'Father Name',
                'lessor_address': 'No. 123, Main Street',
                'lessor_city': 'Chennai',
                'lessor_pincode': '600001',
                'lessee_address': 'No. 456, Second Street',
                'lessee_city': 'Chennai',
                'lessee_pincode': '600002',
                'property_address': 'No. 789, Property Street',
                'property_city': 'Chennai',
                'property_pincode': '600073',
                'lease_period': '2',
                'start_date': '1st April 2024',
                'end_date': '31st March 2026',
                'lease_amount': '25,000',
                'lease_amount_words': 'Twenty Five Thousand',
                'rent_due_date': '1st',
                'security_deposit': '50,000',
                'security_deposit_words': 'Fifty Thousand',
                'notice_period': '3',
                'number_of_rooms': '3'
            })
        
        return defaults
    
    def _generate_fallback_template(self, doc_type, data):
        """Generate a fallback template if file template is not found"""
        if doc_type == 'rental_agreement':
            return f"""
RENTAL AGREEMENT

This Rental Agreement is made on {data.get('date', datetime.now().strftime('%d/%m/%Y'))} between:

LANDLORD: {data.get('landlord', '________________')}
TENANT: {data.get('tenant', '________________')}

PROPERTY: {data.get('address', '________________')}
MONTHLY RENT: {data.get('rent_amount', '________________')}
START DATE: {data.get('start_date', '________________')}
DURATION: {data.get('duration', '________________')} months

Terms and conditions apply as per standard rental agreement.
            """
        elif doc_type == 'land_sale_deed':
            return f"""
LAND SALE DEED

This Sale Deed is executed on {data.get('date', datetime.now().strftime('%d/%m/%Y'))} between:

SELLER: {data.get('seller', '________________')}
BUYER: {data.get('buyer', '________________')}

PROPERTY: {data.get('property_address', '________________')}
SALE AMOUNT: {data.get('sale_amount', '________________')}
SALE DATE: {data.get('sale_date', '________________')}

The seller hereby transfers all rights and ownership to the buyer.
            """
        else:
            return f"Document generated for {doc_type} with provided data: {data}"

# Initialize the processor
processor = LegalDocumentProcessor()

# Ensure custom templates directory exists
CUSTOM_TEMPLATES_DIR = os.path.join('templates', 'custom')
os.makedirs(CUSTOM_TEMPLATES_DIR, exist_ok=True)
CUSTOM_TEMPLATES_VERSIONS_DIR = os.path.join(CUSTOM_TEMPLATES_DIR, 'versions')
os.makedirs(CUSTOM_TEMPLATES_VERSIONS_DIR, exist_ok=True)
TEMPLATE_META_PATH = os.path.join(CUSTOM_TEMPLATES_DIR, '_meta.json')


def _load_template_meta():
    try:
        if os.path.exists(TEMPLATE_META_PATH):
            with open(TEMPLATE_META_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {"favorites": [], "tags": {}, "recents": []}


def _save_template_meta(meta: dict):
    try:
        with open(TEMPLATE_META_PATH, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.context_processor
def inject_supabase_env():
    return {
        'supabase_url': os.environ.get('SUPABASE_URL', ''),
        'supabase_anon_key': os.environ.get('SUPABASE_ANON_KEY', ''),
    }

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/api/process-prompt', methods=['POST'])
def process_prompt():
    """Process user prompt and extract information"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Classify document type
        doc_type = processor.classify_document_type(prompt)
        
        # Extract entities
        entities = processor.extract_entities(prompt)
        
        # Identify missing fields
        missing_fields = processor.identify_missing_fields(doc_type, entities)
        
        # Prepare response
        response = {
            'document_type': doc_type,
            'extracted_entities': entities,
            'missing_fields': missing_fields,
            'status': 'success'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-document', methods=['POST'])
def generate_document():
    """Generate final document with all required data"""
    try:
        data = request.get_json()
        doc_type = data.get('document_type')
        filled_data = data.get('filled_data', {})
        format_type = data.get('format', 'docx')
        language = data.get('language', 'en')
        custom_template_content = data.get('custom_template')
        
        if not doc_type or not filled_data:
            return jsonify({'error': 'Missing required data'}), 400
        
        # Generate document content
        if custom_template_content:
            try:
                template = Template(custom_template_content)
                document_content = template.render(**filled_data)
            except Exception as e:
                return jsonify({'error': f'Error rendering custom template: {str(e)}'}), 400
        else:
            document_content = processor.generate_document(doc_type, filled_data, language=language)
        
        # Create file based on format
        if format_type == 'docx':
            return create_docx_file(document_content, doc_type)
        elif format_type == 'pdf':
            return create_pdf_file(document_content, doc_type)
        else:
            return jsonify({'error': 'Unsupported format'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/templates/list', methods=['GET'])
def list_custom_templates():
    """List available custom templates in templates/custom."""
    try:
        files = [f for f in os.listdir(CUSTOM_TEMPLATES_DIR) if os.path.isfile(os.path.join(CUSTOM_TEMPLATES_DIR, f))]
        return jsonify({'templates': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/templates/get', methods=['GET'])
def get_custom_template():
    """Get the content of a custom template by name."""
    name = request.args.get('name', '')
    if not name:
        return jsonify({'error': 'Missing template name'}), 400
    path = os.path.join(CUSTOM_TEMPLATES_DIR, name)
    if not os.path.isfile(path):
        return jsonify({'error': 'Template not found'}), 404
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return jsonify({'name': name, 'content': f.read()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


ALLOWED_TEMPLATE_EXTENSIONS = {'.txt', '.jinja', '.j2', '.tmpl'}


@app.route('/api/templates/upload', methods=['POST'])
def upload_custom_template():
    """Upload a custom template file into templates/custom."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    filename = secure_filename(file.filename)
    _, ext = os.path.splitext(filename)
    if ext.lower() not in ALLOWED_TEMPLATE_EXTENSIONS:
        return jsonify({'error': 'Unsupported file type'}), 400
    save_path = os.path.join(CUSTOM_TEMPLATES_DIR, filename)
    try:
        file.save(save_path)
        return jsonify({'status': 'success', 'name': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/templates/save', methods=['POST'])
def save_custom_template():
    """Save custom template content by name."""
    data = request.get_json(force=True) or {}
    name = data.get('name')
    content = data.get('content', '')
    if not name:
        return jsonify({'error': 'Missing template name'}), 400
    filename = secure_filename(name)
    if not os.path.splitext(filename)[1]:
        filename += '.txt'
    try:
        # Save current version
        target = os.path.join(CUSTOM_TEMPLATES_DIR, filename)
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        # Save timestamped version copy
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        ver_dir = os.path.join(CUSTOM_TEMPLATES_VERSIONS_DIR, filename)
        os.makedirs(ver_dir, exist_ok=True)
        with open(os.path.join(ver_dir, f'{ts}.txt'), 'w', encoding='utf-8') as vf:
            vf.write(content)
        # Update recents
        meta = _load_template_meta()
        recents = [filename] + [n for n in meta.get('recents', []) if n != filename]
        meta['recents'] = recents[:20]
        _save_template_meta(meta)
        return jsonify({'status': 'success', 'name': filename, 'version': ts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/templates/delete', methods=['POST'])
def delete_custom_template():
    """Delete a custom template by name."""
    data = request.get_json(force=True) or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Missing template name'}), 400
    path = os.path.join(CUSTOM_TEMPLATES_DIR, name)
    if not os.path.isfile(path):
        return jsonify({'error': 'Template not found'}), 404
    try:
        os.remove(path)
        # Clean versions if any
        ver_dir = os.path.join(CUSTOM_TEMPLATES_VERSIONS_DIR, name)
        if os.path.isdir(ver_dir):
            try:
                for f in os.listdir(ver_dir):
                    os.remove(os.path.join(ver_dir, f))
                os.rmdir(ver_dir)
            except Exception:
                pass
        # Update meta
        meta = _load_template_meta()
        meta['recents'] = [n for n in meta.get('recents', []) if n != name]
        meta['favorites'] = [n for n in meta.get('favorites', []) if n != name]
        if name in meta.get('tags', {}):
            meta['tags'].pop(name, None)
        _save_template_meta(meta)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/preview', methods=['POST'])
def preview_render():
    """Render a preview given template content and fields."""
    try:
        data = request.get_json(force=True) or {}
        template_content = data.get('template', '')
        fields = data.get('fields', {})
        if not template_content:
            return jsonify({'error': 'Missing template content'}), 400
        try:
            template = Template(template_content)
            rendered = template.render(**fields)
        except Exception as e:
            return jsonify({'error': f'Render error: {str(e)}'}), 400
        return jsonify({'rendered': rendered})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.get('/api/templates/meta')
def get_template_meta():
    return jsonify(_load_template_meta())


@app.post('/api/templates/meta/update')
def update_template_meta():
    data = request.get_json(force=True) or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Missing template name'}), 400
    meta = _load_template_meta()
    # favorites
    fav = data.get('favorite')
    if fav is not None:
        favs = set(meta.get('favorites', []))
        if fav:
            favs.add(name)
        else:
            favs.discard(name)
        meta['favorites'] = list(favs)
    # tags
    tags = data.get('tags')
    if isinstance(tags, list):
        meta.setdefault('tags', {})[name] = tags
    _save_template_meta(meta)
    return jsonify({'status': 'success', 'meta': meta})


@app.get('/api/templates/search')
def search_templates():
    q = (request.args.get('q') or '').lower().strip()
    meta = _load_template_meta()
    files = [f for f in os.listdir(CUSTOM_TEMPLATES_DIR) if os.path.isfile(os.path.join(CUSTOM_TEMPLATES_DIR, f))]
    results = []
    for f in files:
        tags = [t.lower() for t in meta.get('tags', {}).get(f, [])]
        if not q or q in f.lower() or any(q in t for t in tags):
            results.append({'name': f, 'tags': meta.get('tags', {}).get(f, []), 'favorite': f in meta.get('favorites', [])})
    return jsonify({'results': results})


@app.get('/api/templates/versions')
def list_template_versions():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Missing template name'}), 400
    ver_dir = os.path.join(CUSTOM_TEMPLATES_VERSIONS_DIR, name)
    if not os.path.isdir(ver_dir):
        return jsonify({'versions': []})
    versions = sorted([p[:-4] for p in os.listdir(ver_dir) if p.endswith('.txt')])
    return jsonify({'versions': versions})


@app.post('/api/templates/diff')
def diff_template_versions():
    from difflib import unified_diff
    data = request.get_json(force=True) or {}
    name = data.get('name')
    a = data.get('a')
    b = data.get('b')
    if not all([name, a, b]):
        return jsonify({'error': 'Missing name/a/b'}), 400
    ver_dir = os.path.join(CUSTOM_TEMPLATES_VERSIONS_DIR, name)
    path_a = os.path.join(ver_dir, f'{a}.txt')
    path_b = os.path.join(ver_dir, f'{b}.txt')
    if not (os.path.isfile(path_a) and os.path.isfile(path_b)):
        return jsonify({'error': 'One or both versions not found'}), 404
    with open(path_a, 'r', encoding='utf-8') as fa, open(path_b, 'r', encoding='utf-8') as fb:
        la = fa.read().splitlines()
        lb = fb.read().splitlines()
    diff = '\n'.join(unified_diff(la, lb, fromfile=a, tofile=b, lineterm=''))
    return jsonify({'diff': diff})


@app.get('/api/presets')
def get_presets():
    doc_type = request.args.get('doc_type')
    if not doc_type:
        return jsonify({'error': 'Missing doc_type'}), 400
    try:
        data = processor._get_default_data(doc_type)
        return jsonify({'presets': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Simple clause library stored as JSON
CLAUSES_DIR = os.path.join('templates', 'clauses')
os.makedirs(CLAUSES_DIR, exist_ok=True)
CLAUSES_PATH = os.path.join(CLAUSES_DIR, '_clauses.json')


def _load_clauses():
    try:
        if os.path.exists(CLAUSES_PATH):
            with open(CLAUSES_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save_clauses(items: list):
    with open(CLAUSES_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


@app.get('/api/clauses/list')
def clauses_list():
    return jsonify({'clauses': _load_clauses()})


@app.post('/api/clauses/add')
def clauses_add():
    data = request.get_json(force=True) or {}
    text = (data.get('text') or '').strip()
    tags = data.get('tags') or []
    doc_type = data.get('doc_type')
    jurisdiction = data.get('jurisdiction')
    if not text:
        return jsonify({'error': 'Missing text'}), 400
    items = _load_clauses()
    item = {
        'id': f"c_{len(items)+1}_{int(datetime.now().timestamp())}",
        'text': text,
        'tags': tags,
        'doc_type': doc_type,
        'jurisdiction': jurisdiction
    }
    items.append(item)
    _save_clauses(items)
    return jsonify({'clause': item})


@app.post('/api/clauses/update')
def clauses_update():
    data = request.get_json(force=True) or {}
    cid = data.get('id')
    if not cid:
        return jsonify({'error': 'Missing id'}), 400
    items = _load_clauses()
    for it in items:
        if it.get('id') == cid:
            it['text'] = data.get('text', it['text'])
            it['tags'] = data.get('tags', it.get('tags', []))
            it['doc_type'] = data.get('doc_type', it.get('doc_type'))
            it['jurisdiction'] = data.get('jurisdiction', it.get('jurisdiction'))
            _save_clauses(items)
            return jsonify({'clause': it})
    return jsonify({'error': 'Not found'}), 404


@app.post('/api/clauses/delete')
def clauses_delete():
    data = request.get_json(force=True) or {}
    cid = data.get('id')
    if not cid:
        return jsonify({'error': 'Missing id'}), 400
    items = _load_clauses()
    items = [it for it in items if it.get('id') != cid]
    _save_clauses(items)
    return jsonify({'status': 'success'})


@app.get('/api/clauses/search')
def clauses_search():
    q = (request.args.get('q') or '').lower().strip()
    items = _load_clauses()
    results = []
    for it in items:
        hay = ' '.join([
            it.get('text', ''), ' '.join(it.get('tags', [])),
            it.get('doc_type') or '', it.get('jurisdiction') or ''
        ]).lower()
        if not q or q in hay:
            results.append(it)
    return jsonify({'results': results})


@app.post('/api/clauses/check-duplicates')
def clauses_check_duplicates():
    from difflib import SequenceMatcher
    data = request.get_json(force=True) or {}
    text = (data.get('text') or '').lower()
    items = _load_clauses()
    sims = []
    for it in items:
        ratio = SequenceMatcher(None, text, (it.get('text') or '').lower()).ratio()
        if ratio >= 0.9:
            sims.append({'id': it['id'], 'ratio': ratio, 'text': it['text']})
    return jsonify({'duplicates': sims})

def create_docx_file(content, doc_type):
    """Create DOCX file from content"""
    try:
        doc = Document()
        doc.add_heading(f'{doc_type.replace("_", " ").title()}', 0)
        
        # Add content
        paragraphs = content.split('\n')
        for para in paragraphs:
            if para.strip():
                doc.add_paragraph(para.strip())
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        doc.save(temp_file.name)
        temp_file.close()
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f'{doc_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    
    except Exception as e:
        return jsonify({'error': f'Error creating DOCX: {str(e)}'}), 500

def _ensure_font_for_language(language: str) -> str:
    """Register and return a font name suitable for the specified language."""
    # Default Latin font
    if language == 'ta':
        # Try to register Noto Sans Tamil if available locally under templates/fonts
        fonts_dir = os.path.join('templates', 'fonts')
        noto_tamil_path = os.path.join(fonts_dir, 'NotoSansTamil-Regular.ttf')
        fallback_lohit_path = os.path.join(fonts_dir, 'Lohit-Tamil.ttf')
        try:
            if os.path.exists(noto_tamil_path):
                pdfmetrics.registerFont(TTFont('NotoSansTamil', noto_tamil_path))
                return 'NotoSansTamil'
            if os.path.exists(fallback_lohit_path):
                pdfmetrics.registerFont(TTFont('LohitTamil', fallback_lohit_path))
                return 'LohitTamil'
        except Exception:
            pass
        # If custom Tamil font not found, use Helvetica (will not render Tamil correctly)
        return 'Helvetica'
    return 'Helvetica'

def create_pdf_file(content, doc_type):
    """Create PDF file from plain text content using ReportLab (no external binaries)."""
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()

        doc = SimpleDocTemplate(temp_path, pagesize=A4, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
        styles = getSampleStyleSheet()
        # Choose font based on current request language if present
        req_language = (request.get_json(silent=True) or {}).get('language', 'en')
        pdf_font = _ensure_font_for_language(req_language)

        body_style = ParagraphStyle(
            name='Body',
            parent=styles['Normal'],
            fontName=pdf_font,
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
        )
        title_style = ParagraphStyle(
            name='Title',
            parent=styles['Heading1'],
            fontName=pdf_font,
            fontSize=18,
            leading=22,
            spaceAfter=12,
        )

        story = []
        story.append(Paragraph(doc_type.replace('_', ' ').title(), title_style))
        story.append(Spacer(1, 0.2 * inch))

        # Convert plain text line breaks to simple paragraphs
        for block in content.split('\n\n'):
            block_html = block.strip().replace('\n', '<br/>')
            if not block_html:
                continue
            story.append(Paragraph(block_html, body_style))
            story.append(Spacer(1, 0.12 * inch))

        doc.build(story)

        return send_file(
            temp_path,
            as_attachment=True,
            download_name=f'{doc_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': f'Error creating PDF: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 