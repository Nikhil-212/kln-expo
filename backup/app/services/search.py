from typing import List, Dict, Optional
import os
from ..ir.indexer import build_index, query_index

# Simple in-memory clauses and naive ranking for demo (replace with Whoosh/Elasticsearch)
CLAUSES = [
    {
        "id": "confidentiality-standard",
        "title": "Confidentiality",
        "body": "Each party shall keep Confidential Information in strict confidence...",
        "doc_types": ["nda", "service_agreement"],
        "jurisdictions": ["CA", "NY", "*"],
        "tags": ["confidentiality"],
        "risk_level": "low",
    },
    {
        "id": "term-and-termination",
        "title": "Term and Termination",
        "body": "This Agreement commences on the Effective Date and continues for the Term...",
        "doc_types": ["nda", "service_agreement"],
        "jurisdictions": ["*"],
        "tags": ["term", "termination"],
        "risk_level": "low",
    },
    {
        "id": "governing-law",
        "title": "Governing Law",
        "body": "This Agreement shall be governed by the laws of {{ governing_law }} without regard to conflicts of law principles.",
        "doc_types": ["nda", "service_agreement", "will"],
        "jurisdictions": ["*"],
        "tags": ["governing law"],
        "risk_level": "low",
    },
]


def search_clauses(query: str, doc_type: Optional[str], jurisdiction: Optional[str], top_k: int = 20) -> List[Dict]:
    index_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "index")
    index_dir = os.path.abspath(index_dir)
    # build index if missing
    if not os.path.isdir(index_dir) or not os.listdir(index_dir):
        build_index(index_dir, CLAUSES)

    # query whoosh
    results = query_index(index_dir, query, limit=top_k * 3)

    # filter by doc_type/jurisdiction
    id_to_clause = {c["id"]: c for c in CLAUSES}
    filtered = []
    for r in results:
        c = id_to_clause.get(r["id"])  # best-effort filter using metadata
        if not c:
            continue
        if doc_type and doc_type not in c.get("doc_types", []):
            continue
        if jurisdiction and not (jurisdiction in c.get("jurisdictions", []) or "*" in c.get("jurisdictions", [])):
            continue
        filtered.append(r)

    return filtered[:top_k]

