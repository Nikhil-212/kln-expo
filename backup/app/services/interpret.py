from typing import Dict
import re


DOC_TYPES = {
    "nda": ["non-disclosure", "confidentiality", "nda"],
    "service_agreement": ["service", "consulting", "freelance"],
    "will": ["will", "testament"],
}


def interpret_text(text: str) -> Dict:
    lowered = text.lower()
    chosen_doc = None
    for doc_type, keywords in DOC_TYPES.items():
        if any(k in lowered for k in keywords):
            chosen_doc = doc_type
            break

    jurisdiction = None
    # Very naive jurisdiction detection
    if re.search(r"\bcalifornia\b|\bca\b", lowered):
        jurisdiction = "CA"
    elif re.search(r"\bnew york\b|\bny\b", lowered):
        jurisdiction = "NY"

    required_fields = []
    if chosen_doc == "nda":
        required_fields = ["party_a_name", "party_b_name", "effective_date", "term_months", "governing_law"]
    elif chosen_doc == "service_agreement":
        required_fields = ["client_name", "provider_name", "services_description", "fees", "governing_law"]
    elif chosen_doc == "will":
        required_fields = ["testator_name", "executor_name", "beneficiaries", "date"]

    return {
        "doc_type": chosen_doc,
        "jurisdiction": jurisdiction,
        "required_fields": required_fields,
    }

