import os
from datetime import datetime
import re
import spacy
from jinja2 import Template

# Load spaCy model for NLP processing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

class LegalDocumentProcessor:
    def __init__(self):
        self.document_types = {
            'rental_agreement': {
                'keywords': ['rental', 'rent', 'lease', 'tenant', 'landlord', 'monthly'],
                'required_fields': ['landlord', 'tenant', 'address', 'rent_amount', 'start_date', 'duration'],
                'template': 'rental_agreement_template.txt'
            },
            'land_sale_deed': {
                'keywords': ['sale', 'deed', 'property', 'buyer', 'seller', 'purchase'],
                'required_fields': ['seller', 'buyer', 'property_description', 'sale_amount'],
                'template': 'land_sale_deed_template.txt'
            },
            'power_of_attorney': {
                'keywords': ['power', 'attorney', 'delegate', 'authority', 'behalf'],
                'required_fields': ['grantor', 'attorney', 'powers', 'duration'],
                'template': 'power_of_attorney_template.txt'
            }
        }
        
        self.entity_patterns = {
            'amounts': r'(?:Rs\.?|INR)?\s*(\d+(?:,\d+)*(?:\.\d{2})?)\s*(?:rupees?|Rs\.?|INR)?',
            'dates': r'\d{1,2}[-/]\d{1,2}[-/]\d{4}|\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}',
            'locations': r'\b(?:at|in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            'durations': r'(\d+)\s*(?:year|month|week|day)s?'
        }
