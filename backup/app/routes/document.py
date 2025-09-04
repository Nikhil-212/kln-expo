import os
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from ..auth import login_required
from ..services.document_generator import DocumentGenerator

document_bp = Blueprint('document', __name__)
document_generator = DocumentGenerator()

@document_bp.route('/generate/<doc_type>', methods=['GET', 'POST'])
@login_required
def generate(doc_type):
    valid_types = ['house_lease', 'power_of_attorney', 'land_sale_deed', 'rental_agreement']
    if doc_type not in valid_types:
        flash('Invalid document type selected.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            form_data = request.form.to_dict()
            language = form_data.pop('language', 'en')
            custom_template = form_data.pop('custom_template', None)
            
            # Validate required fields
            missing_fields = document_generator.validate_fields(doc_type, form_data)
            if missing_fields:
                return jsonify({
                    'status': 'missing_fields',
                    'missing_fields': missing_fields
                }), 400

            # Convert numeric fields to the right type
            if doc_type == 'house_lease':
                form_data['rent_amount'] = float(form_data.get('rent_amount', 0))
                form_data['lease_term'] = int(form_data.get('lease_term', 0))
            elif doc_type == 'land_sale_deed':
                form_data['sale_amount'] = float(form_data.get('sale_amount', 0))
            elif doc_type == 'rental_agreement':
                form_data['rental_amount'] = float(form_data.get('rental_amount', 0))
                form_data['agreement_duration'] = int(form_data.get('agreement_duration', 0))
            
            # Generate the document
            document_content = document_generator.generate_document(
                doc_type, 
                form_data, 
                language=language,
                custom_template=custom_template
            )
            
            # Show the generated document
            return render_template('view_document.html', 
                                document_content=document_content,
                                user=session.get('user_id'))
                                
        except Exception as e:
            flash(f'Error generating document: {str(e)}', 'error')
            return redirect(url_for('document.generate', doc_type=doc_type))

    # Get required fields for the document type
    required_fields = document_generator.get_required_fields(doc_type)
    
    return render_template('generate.html', 
                         doc_type=doc_type, 
                         user=session.get('user_id'),
                         required_fields=required_fields)

@document_bp.route('/upload-template', methods=['POST'])
@login_required
def upload_template():
    if 'template' not in request.files:
        return jsonify({'error': 'No template file provided'}), 400
        
    file = request.files['template']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if not file.filename.endswith('.txt'):
        return jsonify({'error': 'Only .txt files are allowed'}), 400
        
    try:
        filename = secure_filename(file.filename)
        content = file.read().decode('utf-8')
        
        # Save the template and get the versioned filename
        new_filename = document_generator.save_custom_template(filename, content)
        
        return jsonify({
            'status': 'success',
            'filename': new_filename,
            'message': f'Template uploaded successfully as {new_filename}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@document_bp.route('/list-custom-templates', methods=['GET'])
@login_required
def list_custom_templates():
    custom_dir = os.path.join(document_generator.custom_template_dir)
    if not os.path.exists(custom_dir):
        return jsonify({'templates': []})
        
    templates = [f for f in os.listdir(custom_dir) 
                if f.endswith('.txt') and os.path.isfile(os.path.join(custom_dir, f))]
                
    return jsonify({'templates': templates})
