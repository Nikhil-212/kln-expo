from typing import List


def validate_draft(doc_type: str, jurisdiction: str, text: str) -> List[dict]:
    issues = []

    # Presence checks
    if doc_type == "nda":
        if "Confidential" not in text and "confidential" not in text.lower():
            issues.append({
                "id": "nda-confidentiality-missing",
                "severity": "error",
                "message": "NDA should include a confidentiality clause."
            })
        if "govern" not in text.lower():
            issues.append({
                "id": "governing-law-missing",
                "severity": "warning",
                "message": "Consider adding a governing law clause."
            })

    # Jurisdictional example rule
    if jurisdiction == "CA":
        if "california" not in text.lower():
            issues.append({
                "id": "jurisdiction-mention",
                "severity": "info",
                "message": "Document governed by CA should mention California."
            })

    return issues

